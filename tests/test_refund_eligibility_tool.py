"""Offline checks for the additional HW1 tool, using temporary course data."""

import asyncio
import json
import sqlite3
from datetime import timedelta
from pathlib import Path

import pytest
from agents.tool_context import ToolContext

from agent import db
from agent.agent import TOOLS_BY_ROLE
from agent.auth import AuthContext
from agent.tools import check_refund_eligibility, check_refund_eligibility_logic

SHOPPER = AuthContext(user_id=1, role="shopper")


@pytest.mark.parametrize(
    "order_id,eligible,approval",
    [(4127, True, False), (3980, False, False), (4455, True, True)],
)
def test_demo_results_do_not_change_database(world_copy: Path, order_id, eligible, approval):
    before = world_copy.read_bytes()
    result = check_refund_eligibility_logic(SHOPPER, order_id)
    assert result["ok"] is True
    assert result["eligible"] is eligible
    assert result["full_refund_requires_approval"] is approval
    if order_id == 3980:
        assert result["reason"] == "The order is outside the return window."
    assert world_copy.read_bytes() == before


@pytest.mark.parametrize("ctx", [
    AuthContext(user_id=2, role="shopper"),
    AuthContext(user_id=9002, role="merchant", store_id=2),
])
def test_denial_has_no_private_order_fields(world_copy: Path, ctx):
    result = check_refund_eligibility_logic(ctx, 4127)
    assert result == {
        "ok": False, "error": "permission_denied",
        "reason": "You do not have permission to check this order.",
    }


@pytest.mark.parametrize("ctx", [
    AuthContext(user_id=9001, role="merchant", store_id=1),
    AuthContext(user_id=9501, role="support"),
])
def test_authorized_roles(world_copy: Path, ctx):
    assert check_refund_eligibility_logic(ctx, 4127)["eligible"] is True


def test_unknown_order(world_copy: Path):
    assert check_refund_eligibility_logic(SHOPPER, -1)["error"] == "not_found"


@pytest.mark.parametrize("age,eligible", [(14, True), (15, False)])
def test_store_override_boundary(world_copy: Path, age, eligible):
    with db.connection() as conn:
        today = db.world_asof(conn)
    with sqlite3.connect(world_copy) as conn:
        conn.execute("UPDATE stores SET return_window_days_override = 14 WHERE id = 1")
        conn.execute("UPDATE orders SET delivered_at = ? WHERE id = 4127",
                     ((today - timedelta(days=age)).isoformat(),))
    result = check_refund_eligibility_logic(SHOPPER, 4127)
    assert result["eligible"] is eligible
    assert result["return_window_days"] == 14
    assert "cw-store-overrides" in result["policy_ids"]


@pytest.mark.parametrize("status,delivery,flag", [
    ("refunded", "2026-06-19", 1),
    ("delivered", None, 1),
    ("delivered", "2099-01-01", 1),
    ("delivered", "2026-06-19", 0),
])
def test_invalid_or_stale_state_cannot_claim_eligibility(world_copy: Path, status, delivery, flag):
    with sqlite3.connect(world_copy) as conn:
        conn.execute("UPDATE orders SET status = ?, delivered_at = ?, refund_eligible = ? WHERE id = 4127",
                     (status, delivery, flag))
    assert check_refund_eligibility_logic(SHOPPER, 4127)["eligible"] is False


def test_registered_tool_can_be_called_without_a_model(world_copy: Path):
    for role in ("shopper", "merchant", "support"):
        assert check_refund_eligibility in TOOLS_BY_ROLE[role]
    result = asyncio.run(check_refund_eligibility.on_invoke_tool(
        ToolContext(context=SHOPPER, tool_name="check_refund_eligibility",
                    tool_call_id="offline-check", tool_arguments='{"order_id": 3980}'),
        json.dumps({"order_id": 3980})
    ))
    assert result["eligible"] is False
