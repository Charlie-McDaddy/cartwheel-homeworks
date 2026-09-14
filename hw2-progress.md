# Homework 2 progress

The user reports that `uv sync` completed. Its output has not been checked.

## Work and checks

- [x] Part A: added authenticated caller and permission fields to tool spans in `observability/instrument.py`.
- [x] Part A: `git diff --check` passed.
- [ ] Part A behavior remains untested.
- [x] Part B: implemented session creation in `server/app.py`.
- [x] Part B: focused session creation test passed (user-reported: 1 passed, 40 deselected).
- [x] Part C: implemented the traced message endpoint in `server/app.py`.
- [ ] Part C behavior remains untested.
- [x] Part C: added Langfuse session association with `propagate_attributes`, while keeping `cartwheel.session_id`.
- [ ] The Langfuse session association change remains untested.
- [x] Part D: added offline authentication tests in `tests/test_observability.py`.
- [ ] Part D tests remain unrun; the full suite remains unrun.
- [ ] Part E: send at least five live requests and inspect the traces.
- [ ] Part F: compare two prompt versions with controlled requests.

## Latest test run

- The user reports that the most recent full suite had 153 passed, 13 skipped, 21 xfailed, and 9 xpassed.
- The Langfuse session association change was made after that run and remains untested.
- The offline Module 2 fixture now clears inherited Langfuse settings. This change is untested.

## Trace usage diagnosis

- A read-only fetch of observation `80e77bfab5bfc213` returned empty `usage_details`, legacy input/output token counts of zero, and no saved model output. This describes the stored observation; it does not prove whether the provider returned usage.
- Added a local compatibility processor for LiteLLM generation-span usage and output recording, plus an offline regression test. The test is unrun, and no provider call was made.

## Deliverables

- [ ] `observability/instrument.py`
- [ ] `server/app.py`
- [ ] `tests/test_observability.py`
- [ ] `hw2-traces.json` with exactly two selected traces
- [ ] Student-recorded video of no more than 5 minutes

The student must record the video and complete the assessments. These remain pending.
