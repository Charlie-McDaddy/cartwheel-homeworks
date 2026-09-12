# Homework 1 video checklist

Status: recording pending. Record one continuous video of at most five minutes.
Explain the results in your own words. This checklist is a guide, not a script.

## Suggested order

- [ ] Show the saved shopper lookup for order 4127 in `hw1-session.jsonl`. Point to the successful tool result and the displayed order.
- [ ] Show the merchant user 9002 request for order 4127. Point to `permission_denied` and the response.
- [ ] Show the saved order-4455 refund conversation. Explain what the tools actually did: the refund was queued for human approval and a demo support ticket was created. No real money moved.
- [ ] Show `hw1-prompt-comparison.json`. Explain ESC-2: all account changes must go to a human. Show the failed before response, the exact added instruction in `agent/agent.py`, and the successful `escalate_to_human` result after the change.
- [ ] Run the focused test command below.
- [ ] Run the record-count command below.

Run commands from the repository root:

```bash
uv run pytest --runxfail tests/test_hw_holes.py -k hw1
```

```bash
uv run python -c 'import json; from pathlib import Path; rows = [json.loads(line) for line in Path("hw1-session.jsonl").read_text().splitlines() if line.strip()]; print(len(rows))'
```

Expected results at preparation time: six focused tests pass; ten conversation records.
The matched prompt comparison is saved separately and does not inflate that count.

## Evidence limits

The tickets are local demo records, not messages to real support staff.
The new refund eligibility tool passed offline tests. It has not yet been used in a live model chat.
One successful email-change retest does not prove that every account-change request will succeed.
The dragon-poem failure remains in the saved conversations; this prompt edit addresses account changes only.
The after response did not cite a policy document for the follow-up time. The student's pass assessment concerns ESC-2.

## Files for the homework

- `agent/tools.py`: required tools and the additional refund eligibility tool.
- `agent/agent.py`: tool registration and the account-change instruction.
- `hw1-session.jsonl`: ten assessed conversations.
- `hw1-prompt-comparison.json`: exact before/after responses, tool calls, instructions, and student assessments.
- `tests/test_hw_holes.py` and `tests/test_refund_eligibility_tool.py`: offline checks.

Keep `.env` private. Keep local progress notes separate from the submission.
Publishing, submission, and video recording remain the student's steps.
