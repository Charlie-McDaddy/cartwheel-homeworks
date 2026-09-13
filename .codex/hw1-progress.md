# HW1 tutorial progress

## Current status

- Student assessed the revised email-change response “yes”: ESC-2 passed. The baseline was assessed as failed. Both exact captures and prompts are saved in `hw1-prompt-comparison.json`.
- The matched after run called escalate_to_human and created local demo ticket 151. This is not a real support handoff. One successful comparison does not prove general reliability; the after response's uncited SLA is separate from the ESC-2 assessment.
- Ten assessed conversations across all three roles remain in `hw1-session.jsonl`. Final offline artifact validation passed. The dragon failure is preserved; the prompt edit addresses account changes only.
- After the prompt edit, six focused HW1 tests and 39 additional-tool/required regression tests passed, all offline. `git diff --check` passed. No further code edits followed those checks.
- Local commit created: `16bfbcd` — Complete HW1 tools and record evaluated support conversations. Includes agent/tools.py, agent/agent.py, tests/test_hw_holes.py, tests/test_refund_eligibility_tool.py, hw1-session.jsonl, hw1-prompt-comparison.json, hw1-video-checklist.md.
- Existing unrelated changes in .env.example, README.md, SPEC.md, and agent/cli.py were left outside the commit. Local .codex notes and .env were not committed. No push occurred.
- Next step: student records one continuous video of at most five minutes using `hw1-video-checklist.md`, explains their observations, and submits/publishes when ready. Video is pending; do not mark the full homework complete until the student records it.

## Deliverable checklist

- [x] Verify all five required tools with the full focused HW1 test command: 6 passed.
- [x] Choose, implement, register, and test the additional refund eligibility tool: 15 offline tests passed.
- [x] Save at least 10 assessed conversations across all three roles. Ten saved, including the required shopper order-4127 lookup.
- [x] Investigate the email-change omission with a matched live before/after test and student assessments. Preserve the separate dragon failure.
- [x] Run final required offline checks and validate submission records: 45 checks passed; ten records and comparison validated.
- [x] Create local homework commit 16bfbcd, excluding secrets and unrelated files.
- [ ] Student records the required continuous video of at most five minutes.

## Evidence

- Repository root: `/Users/charliemac/Desktop/Coding/cartwheel-homeworks`.
- `python3 --version`: `Python 3.14.7`.
- `uv --version`: `uv 0.11.29`.
- `SPEC.md` defines the Cartwheel scope, role permissions, tool contracts, escalation rules, and response rules.
- `agent/agent.py` renders the model system prompt and registers tools by role.
- At initial setup, `agent/tools.py` contained five HW1 `NotImplementedError` stubs (now implemented): `get_policy`, `search_products`, `list_my_orders`, `cancel_order`, and `find_order`.
- `uv sync` completed with Python 3.12.9 and the locked dependencies.
- `uv run python -m seed.generate` completed at development scale and pinned demo orders #4127, #3980, and #4455.
- `uv run pytest` completed: 109 passed, 12 skipped, 27 expected failures (`xfail`).
- Credential check on 2026-09-08: the OpenRouter key is present; its value was not printed. One live model request was run through the `openrouter` alias.
- The live CLI conversation ran as shopper user 1 with request: `Please look up order 4127 and show me its details.` The CLI exited with status 0 after `quit`.
- Observed tool call: `get_order({"order_id": 4127})` returned `ok: true` and order 4127 for Blue Heron Ceramics, total `$84.00`, status `delivered`, ordered `2026-06-14`, shipped `2026-06-16`, delivered `2026-06-19`, and `refund_eligible: true`.
- Observed final response displayed the order number, store, product ID 1, quantity 1, total, status, dates, and refund eligibility. It did not include progress messages before the tool call.
- This run used `--debug`; the CLI output is the source for the actual tool call, result, and response. No live trace was enabled.
- Student prediction before the first HW1 tool implementation, recorded exactly: “I would expect the agent to reply that they could not find a policy with that ID.”
- Student prediction for the empty `search_products` query, recorded exactly: “if the customer gives an empty search the chatbot should not return and information but prompt the user to provide product search words”.
- Student prediction before `list_my_orders`, recorded exactly: “the agent should show all relevant orders to a shopper”. The contract qualifies “all” as at most 20 records, newest first.
- Implemented `get_policy` only. It returns the matching policy fields for an exact, case-sensitive ID and a structured `not_found` result naming the requested ID.
- Actual missing-ID tool output: `{'ok': False, 'error': 'not_found', 'reason': "No policy found with id 'cw-does-not-exist'."}`.
- Implemented `search_products` only. It validates blank queries and nonpositive price ceilings, resolves an optional store by name or slug, matches every query token in title or description, filters by inclusive price ceiling, clamps limits to 1 through 25, and sorts by price then product ID.
- Actual empty-query tool output: `{'ok': False, 'error': 'invalid_argument', 'reason': 'Please provide product search words.'}`.
- Implemented `list_my_orders`. Shoppers use `list_orders_for_user`; merchants use `list_orders_for_store` with their authenticated `store_id`; support receives structured `invalid_argument` explaining that `get_order` is for specific order lookup. Results use `Order.to_public_dict()`, include `count`, and use the supplied 20-record newest-first query limit.
- Student prediction before `cancel_order`, recorded exactly: “if a shopper tries to cancel an order that has already shipped, tell the user, sorry the order has already shipped and refer to human for further assistance.”
- Implemented `cancel_order`. It checks the kill switch first, then returns `not_found` for an unknown order, checks authorization before status, allows only `placed` orders, and persists `cancelled` through `db.set_order_status`.
- Offline focused contract check: `UV_CACHE_DIR=/private/tmp/cartwheel-uv-cache uv run pytest tests/test_hw_holes.py -k hw1_cancel_order --runxfail` passed (1 passed).
- Offline handout regressions: `UV_CACHE_DIR=/private/tmp/cartwheel-uv-cache uv run pytest tests/test_agent_tools.py tests/test_auth.py tests/test_eligibility.py` passed (24 passed).
- Temporary database checks observed shipped order 4127 returning `not_eligible` with current status `delivered` and staying `delivered`; an unauthorized shopper returned `permission_denied`; `CARTWHEEL_KILL_SWITCH=readonly` returned `paused` and left a placed order unchanged; an authorized shopper changed a placed order to `cancelled` in a separate temporary copy.
- The tool contract returns a structured `not_eligible` result. Human referral is a separate model decision handled by `escalate_to_human`; no automatic ticket or external side effect was added.
- Database evidence for the live merchant test: user 9002 is role `merchant`, store 2; order 4127 belongs to store 1. The main database was read only and no mutation was observed.
- Offline focused contract check: `UV_CACHE_DIR=/private/tmp/cartwheel-uv-cache uv run pytest tests/test_hw_holes.py -k hw1_search_products --runxfail` passed (1 passed).
- Offline focused list-orders check: `UV_CACHE_DIR=/private/tmp/cartwheel-uv-cache uv run pytest tests/test_hw_holes.py -k hw1_list_my_orders --runxfail` passed (1 passed).
- Offline regression checks: `UV_CACHE_DIR=/private/tmp/cartwheel-uv-cache uv run pytest tests/test_agent_tools.py tests/test_db.py tests/test_auth.py tests/test_seed_determinism.py -q` passed (31 passed).
- Required handout regression: `UV_CACHE_DIR=/private/tmp/cartwheel-uv-cache uv run pytest tests/test_agent_tools.py tests/test_auth.py tests/test_eligibility.py` passed (24 passed).
- Manual offline examples: shopper user 1 returned 20 orders newest first, beginning with order 4455; merchant user 9001/store 1 returned 20 store orders newest first, beginning with order 6213; support user 9501 returned `invalid_argument` with no order data.

