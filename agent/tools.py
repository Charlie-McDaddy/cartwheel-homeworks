"""Homework 1: the remaining commerce-agent tools.

The three lecture tools (`search_help_center`, `get_order`, `issue_refund`)
are implemented in agent/agent.py and are worked examples of the pattern:
check permissions first, go through agent/db.py for data, and return a
structured dict, never a prose error. The homework tools follow the same
pattern. agent/agent.py already wraps each function below as an SDK tool, so
once a function works here it works in chat with no further wiring.

Result convention (see agent/auth.py):
  - Success: a dict with "ok": True plus the payload fields named in each
    docstring.
  - Failure: {"ok": False, "error": <code>, "reason": <human-readable str>}.

Run the contract tests with: uv run pytest tests/test_hw_holes.py -k hw1
They are marked xfail and flip to passing as you implement each function.
"""

from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any

from agents import RunContextWrapper, function_tool

from agent import db
from agent.auth import AuthContext, can_cancel_order, can_refund_order, permission_denied
from agent.config import load_facts
from agent.helpcenter import load_policy_docs
from agent.killswitch import kill_switch
from observability.instrument import record_tool_result
from seed.eligibility import effective_return_window_days, is_refund_eligible, refund_needs_approval

MAX_SEARCH_LIMIT = 25
DEFAULT_ORDER_LIMIT = 20
FIND_ORDER_STOPWORDS = {
    "and", "bought", "from", "have", "last", "my", "order", "the", "week",
}


def check_refund_eligibility_logic(ctx: AuthContext, order_id: int) -> dict[str, Any]:
    """Check full-order refund eligibility without writing any records.

    Check access before returning eligibility or order facts. A successful
    check returns eligible, reason, policy_ids, and whether a full refund
    would need human approval. It never promises payment or creates a ticket.
    Missing store data or inconsistent eligibility needs human review.
    """
    with db.connection() as conn:
        order = db.get_order(conn, order_id)
        if order is None:
            return {"ok": False, "error": "not_found", "reason": "Order not found."}
        if not can_refund_order(ctx, order.user_id, order.store_id):
            return permission_denied("You do not have permission to check this order.")
        store = db.get_store(conn, order.store_id)
        if store is None:
            return {"ok": False, "error": "invalid_argument",
                    "reason": "Store information is missing. A human must review this order."}
        facts = load_facts()
        today = db.world_asof(conn)
        window = effective_return_window_days(
            facts["return_window_days"], store.return_window_days_override
        )
        computed = is_refund_eligible(
            status=order.status, delivered_at=order.delivered_at,
            as_of=today, return_window_days=window,
        )
        eligible = computed and order.refund_eligible
        if order.status != "delivered":
            reason = f"The order status is {order.status}; only delivered orders qualify."
        elif order.delivered_at is None or order.delivered_at > today:
            reason = "Delivery information is missing or inconsistent. A human must review it."
        elif not computed:
            reason = "The order is outside the return window."
        elif not order.refund_eligible:
            reason = "The order is marked ineligible despite meeting the date rules. A human must review it."
        else:
            reason = "The order meets the refund eligibility rules. This check does not issue a refund."
        policy_ids = ["cw-returns", "cw-refunds"]
        if store.return_window_days_override is not None:
            policy_ids.extend(["cw-store-overrides", f"store-{store.slug}-policy"])
        return {
            "ok": True, "order_id": order.id, "eligible": eligible,
            "reason": reason, "return_window_days": window,
            "full_refund_amount_usd": order.total_usd,
            "full_refund_requires_approval": eligible and refund_needs_approval(
                order.total_usd, facts["refund_auto_approve_threshold_usd"]
            ),
            "policy_ids": policy_ids,
        }


@function_tool(failure_error_function=None)
def check_refund_eligibility(
    wrapper: RunContextWrapper[AuthContext], order_id: int
) -> dict[str, Any]:
    """Check whether an accessible order qualifies for a full refund and why.

    Read only: does not issue a refund or open a support ticket. Returns
    eligibility, policy identifiers, and whether a full refund needs human
    approval. Fetch the cited policies for policy details. An eligible result
    is not a payment confirmation; issuing a refund remains a separate action.
    """
    result = check_refund_eligibility_logic(wrapper.context, order_id)
    record_tool_result(wrapper.context, result)
    return result


def get_policy(ctx: AuthContext, policy_id: str) -> dict[str, Any]:
    """Fetch one policy doc by its exact id. Risk tier: read.

    Every role may read every policy doc (the corpus is public help-center
    content), so this tool needs no permission check.

    Args:
        ctx: The caller's auth context. Unused here, but every tool takes it.
        policy_id: An exact policy id, e.g. "cw-returns" or
            "store-juniper-home-goods-policy". Matching is exact and
            case-sensitive; ids are the `policy_id` front-matter field of the
            files in data/policies/.

    Returns:
        On success: {"ok": True, "policy_id": str, "title": str,
        "audience": str, "body": str} where body is the markdown body of the
        doc without the front matter.
        If no doc has that id: {"ok": False, "error": "not_found",
        "reason": ...} naming the id that was requested.

    Implementation notes:
        agent.helpcenter.load_policy_docs() returns every parsed doc.
    """
    for doc in load_policy_docs():
        if doc.policy_id == policy_id:
            return {
                "ok": True,
                "policy_id": doc.policy_id,
                "title": doc.title,
                "audience": doc.audience,
                "body": doc.body,
            }
    return {
        "ok": False,
        "error": "not_found",
        "reason": f"No policy found with id {policy_id!r}.",
    }


def search_products(
    ctx: AuthContext,
    query: str,
    store: str | None = None,
    max_price_usd: float | None = None,
    limit: int = 5,
) -> dict[str, Any]:
    """Search the product catalog. Risk tier: read.

    Every role may search products. Matching is deterministic keyword
    matching, not semantic search: a product matches when every whitespace
    token of `query` appears case-insensitively as a substring of the
    product's title or description.

    Args:
        ctx: The caller's auth context.
        query: Free-text query. Must be non-empty after stripping whitespace;
            otherwise return {"ok": False, "error": "invalid_argument",
            "reason": ...}.
        store: Optional store filter. Matched with
            agent.db.get_store_by_name (case-insensitive name or slug). If
            given and no store matches, return {"ok": False, "error":
            "not_found", "reason": ...} naming the store string.
        max_price_usd: Optional inclusive price ceiling. If given and not
            strictly positive, return an "invalid_argument" error.
        limit: Maximum products to return. Clamp to the range
            [1, MAX_SEARCH_LIMIT]; do not error on out-of-range values.

    Returns:
        {"ok": True, "products": [...], "count": <len(products)>} where each
        product is {"product_id": int, "store_id": int, "title": str,
        "price_usd": float}. Sort matches by price_usd ascending, then by
        product_id ascending, and truncate to `limit`. No matches is still a
        success: {"ok": True, "products": [], "count": 0}.

    Implementation notes:
        agent.db.list_products(conn, store_id) gives the candidate set.
        Use `with db.connection() as conn:` to close the database automatically.
    """
    query_tokens = query.strip().casefold().split()
    if not query_tokens:
        return {
            "ok": False,
            "error": "invalid_argument",
            "reason": "Please provide product search words.",
        }
    if max_price_usd is not None and max_price_usd <= 0:
        return {
            "ok": False,
            "error": "invalid_argument",
            "reason": "max_price_usd must be strictly positive.",
        }

    result_limit = max(1, min(MAX_SEARCH_LIMIT, limit))
    with db.connection() as conn:
        store_id: int | None = None
        if store is not None:
            matched_store = db.get_store_by_name(conn, store)
            if matched_store is None:
                return {
                    "ok": False,
                    "error": "not_found",
                    "reason": f"No store found matching {store!r}.",
                }
            store_id = matched_store.id

        products = db.list_products(conn, store_id)

    matches = [
        product
        for product in products
        if all(
            token in f"{product.title} {product.description}".casefold()
            for token in query_tokens
        )
        and (max_price_usd is None or product.price_usd <= max_price_usd)
    ]
    matches.sort(key=lambda product: (product.price_usd, product.id))
    matches = matches[:result_limit]
    return {
        "ok": True,
        "products": [
            {
                "product_id": product.id,
                "store_id": product.store_id,
                "title": product.title,
                "price_usd": product.price_usd,
            }
            for product in matches
        ],
        "count": len(matches),
    }


def list_my_orders(ctx: AuthContext) -> dict[str, Any]:
    """List recent orders in the caller's own scope. Risk tier: read.

    Role behavior, straight from the access matrix in SPEC.md:
        - shopper: the caller's own orders.
        - merchant: the caller's store's orders (ctx.store_id).
        - support: support staff have no orders of their own and look up
          specific orders with get_order instead, so return {"ok": False,
          "error": "invalid_argument", "reason": ...} saying exactly that.

    Returns:
        For shopper and merchant: {"ok": True, "orders": [...],
        "count": <len(orders)>} where each order is
        agent.db.Order.to_public_dict() and the list holds at most
        DEFAULT_ORDER_LIMIT orders, newest first (agent.db.list_orders_for_user
        and list_orders_for_store already sort and limit this way).

    Implementation notes:
        No permission check is needed beyond the role dispatch, because the
        scope is baked into which query you run. That is the point of the
        tool: the model cannot ask for someone else's orders through it.
    """
    if ctx.role == "support":
        return {
            "ok": False,
            "error": "invalid_argument",
            "reason": (
                "Support callers cannot list orders; use get_order for a "
                "specific order instead."
            ),
        }

    with db.connection() as conn:
        if ctx.role == "shopper":
            orders = db.list_orders_for_user(conn, ctx.user_id, DEFAULT_ORDER_LIMIT)
        else:
            orders = db.list_orders_for_store(conn, ctx.store_id, DEFAULT_ORDER_LIMIT)

    public_orders = [order.to_public_dict() for order in orders]
    return {"ok": True, "orders": public_orders, "count": len(public_orders)}


def cancel_order(ctx: AuthContext, order_id: int, reason: str) -> dict[str, Any]:
    """Cancel an order. Risk tier: write.

    This is the homework's write tool, and it must enforce two independent
    rules in this order:

    1. The access matrix (scope): use agent.auth.can_cancel_order. Shoppers
       may cancel only their own orders, merchants only their own store's
       orders, support any order. On failure return
       agent.auth.permission_denied(...) with a reason naming the role and
       the order id. Scope is checked before the status rule so that an
       out-of-scope caller learns nothing about the order's state.
    2. The pre-shipment rule (facts.yaml `cancel_cutoff`): only orders whose
       status is exactly "placed" can be cancelled, for every role. If the
       order is in scope but its status is not "placed", return
       {"ok": False, "error": "not_eligible", "reason": ...} that names the
       current status and states that orders can be cancelled only before
       shipment.

    Args:
        ctx: The caller's auth context.
        order_id: The order to cancel.
        reason: Free-text reason from the user; not validated.

    Returns:
        If no order has this id: {"ok": False, "error": "not_found",
        "reason": ...}.
        On success: {"ok": True, "order_id": order_id, "status": "cancelled"}
        after persisting the new status with agent.db.set_order_status.

    Implementation notes:
        Fetch with agent.db.get_order. Note the argument order of
        can_cancel_order(ctx, order_user_id, order_store_id).

    The Module 4 kill switch is checked first (before the scope and
    status rules and before your code), so that a paused write tool touches
    nothing. It is provided; the default ("off") returns None and falls
    through to your implementation.
    """
    paused = kill_switch("cancel_order")
    if paused is not None:
        return {"ok": False, "error": "paused", "reason": paused}

    with db.connection() as conn:
        order = db.get_order(conn, order_id)
        if order is None:
            return {
                "ok": False,
                "error": "not_found",
                "reason": f"No order found with id {order_id}.",
            }

        if not can_cancel_order(ctx, order.user_id, order.store_id):
            return permission_denied(
                f"Role {ctx.role!r} cannot cancel order {order_id}."
            )

        if order.status != "placed":
            return {
                "ok": False,
                "error": "not_eligible",
                "reason": (
                    f"Order {order_id} has status {order.status!r}; "
                    "orders can be cancelled only before shipment."
                ),
            }

        db.set_order_status(conn, order_id, "cancelled")

    return {"ok": True, "order_id": order_id, "status": "cancelled"}


def find_order(ctx: AuthContext, query: str) -> dict[str, Any]:
    """Search the caller's orders by product name. Risk tier: read.

    Takes a natural-language query (e.g., "earmuffs I bought last week")
    and searches the authenticated user's orders for products whose name
    matches. Use fuzzy string matching (e.g., thefuzz.fuzz.partial_ratio
    or SQLite LIKE) to find orders whose product name is close to the
    query.

    Access rules: a shopper searches only the shopper's own orders, a
    merchant searches orders from the merchant's store, and support staff
    can search any orders. Use agent.db.list_orders_for_user for shoppers
    and agent.db.list_orders_for_store for merchants. For support staff,
    use agent.db.list_orders_for_user with no user filter, or search
    across all orders.

    Args:
        ctx: The caller's auth context.
        query: A natural-language description of the product.

    Returns:
        {"ok": True, "orders": [...]} with a list of matching orders
        (at most 5), each as the dict returned by agent.db. If no orders
        match, return {"ok": True, "orders": []}.
    """
    # Product names are the only searchable order detail.  Ignore short
    # conversational words so a query such as "earmuffs I bought last week"
    # is matched against the product name rather than the whole sentence.
    query_tokens = [
        token.casefold()
        for token in query.split()
        if len(token) >= 3 and token.casefold() not in FIND_ORDER_STOPWORDS
    ]
    if not query_tokens:
        return {"ok": True, "orders": []}

    with db.connection() as conn:
        if ctx.role == "shopper":
            # SQLite treats LIMIT -1 as unlimited, so older orders are not
            # hidden by the helper's normal 20-order display limit.
            scoped_orders = db.list_orders_for_user(conn, ctx.user_id, -1)
        elif ctx.role == "merchant":
            scoped_orders = db.list_orders_for_store(conn, ctx.store_id, -1)
        else:
            # list_orders_for_user intentionally requires a user filter.  A
            # A support caller is authorized for cross-order lookup, so this
            # read-only query supplies the missing unfiltered candidate set.
            rows = conn.execute("SELECT id FROM orders").fetchall()
            scoped_orders = [db.get_order(conn, row["id"]) for row in rows]
            scoped_orders = [order for order in scoped_orders if order is not None]

        products_by_id = {product.id: product for product in db.list_products(conn)}
        matches: list[tuple[float, Any]] = []
        for order in scoped_orders:
            product = products_by_id.get(order.product_id)
            if product is None:
                continue
            title = product.title.casefold()
            title_tokens = title.split()
            scores = []
            for token in query_tokens:
                if token in title:
                    scores.append(1.0)
                else:
                    scores.append(
                        max(
                            (SequenceMatcher(None, token, title_token).ratio()
                             for title_token in title_tokens),
                            default=0.0,
                        )
                    )
            score = sum(scores) / len(scores)
            if score >= 0.65:
                matches.append((score, order))

    matches.sort(key=lambda item: (-item[0], -item[1].ordered_at.toordinal(), -item[1].id))
    return {"ok": True, "orders": [order.to_public_dict() for _, order in matches[:5]]}
