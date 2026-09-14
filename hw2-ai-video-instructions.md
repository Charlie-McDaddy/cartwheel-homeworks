# Homework 2: AI video brief and voice script

## Copy this brief to the video assistant

Help a student prepare a clear screen demonstration of Homework 2 in the Cartwheel course. Explain the work for a viewer with no programming background. Use the real application, saved traces, and actual test output.

The course requires one continuous screen recording of no more than five minutes. The student must make the recording and own the explanations and assessments. Prepare the scene plan, cue sheet, and narration below for that recording. You may make a clearly labelled rehearsal video with an ordinary synthetic voice. Do not present a generated rehearsal as the student's required recording. Do not invent application footage, successful tests, trace details, or personal assessments.

Target length: 4 minutes 40 seconds, with 20 seconds spare. If a step takes longer, shorten the spoken explanation. Do not speed up or cut the required continuous recording to hide waiting or errors.

## Readiness: resolve these before the final recording

This brief is ready for rehearsal. The submission evidence still needs these checks:

1. **Correct the trace identifiers and links.** The current `hw2-traces.json` contains `f9bb77c0cf092001` and `aa4cfa37b56010c9`. These are root-span observation IDs from the pasted exports. They were incorrectly labelled as whole-trace IDs. The two `http://localhost:3000/trace/...` links were guessed and have not been verified. Open the two real traces in Langfuse. Copy each actual trace ID and its working browser URL. Verify both links before updating the JSON file. Do not derive a trace ID from a session ID or span ID. The earlier JSON check verified structure only; it did not verify the links or identities.

2. **Resolve the Part F comparison requirement.** The observed wording experiment changed `Plain and warm. No legalese.` to `Plain, warm, and concise. No legalese.` The original hash was `b24e1d226ef2`. The student reported `0c8cc1a41e4b` for the changed prompt. The handout asks for the earlier Homework 1 prompt when Homework 1 produced a revision. It permits a small wording change when there was no HW1 revision. This project did have an HW1 revision. Repeat the comparison with that earlier prompt before claiming full compliance, unless the instructor explicitly accepts the wording experiment. Use the same user, request, model, empty history, and database state. Restore the current prompt afterward. Do not reset the student's database without checking what would be lost.

3. **Find both comparison traces.** The original comparison trace export is available locally. The second hash was reported by the student, but the second full trace was not supplied here. Locate both traces in Langfuse and show the actual hashes. Do not manufacture the second trace from the reported hash. If the comparison is repeated, update the script with the newly verified hashes.

4. **Verify the local recording setup.** Confirm the two selected traces, both comparison traces, and the terminal are ready. Check the real test result during rehearsal. The student previously reported `153 passed, 13 skipped, 21 xfailed, 9 xpassed`; that is historical, user-reported evidence, not a fresh run. Some lines in `hw2-progress.md` are stale, so do not use that file alone to certify completion.

The video assistant must explain these remaining checks. It must not silently change the submission file, restart services, run models, or create new evidence. Follow the student's one-step-at-a-time approval rule for such actions.

## Local files and evidence

Repository root:

`/Users/charliemac/Desktop/Coding/cartwheel-homeworks`

Authoritative requirements:

- `AGENTS.md`
- `homework/module-1/hw2.md`, especially Parts E and F, Trace record, Files to commit, and Video
- `SPEC.md`

Implementation and test files:

- `server/app.py`: identity checks, sessions, tokens, and the traced message route
- `observability/instrument.py`: tool attributes and generation-span compatibility helper
- `tests/test_observability.py`: authentication and tracing checks
- `hw2-traces.json`: two selected trace records; identifiers and links still need correction

Saved shopper trace export:

`/Users/charliemac/.codex/attachments/531aa485-fe15-4c56-84ae-ae8d4afb3313/pasted-text.txt`

Saved merchant trace export:

`/Users/charliemac/.codex/attachments/ac458f69-f5a6-4420-a048-5e1ebdae80fb/pasted-text.txt`

Original prompt-comparison trace export:

`/Users/charliemac/.codex/attachments/6bdb52bd-9701-4f25-ba35-26755d43b6dd/pasted-text.txt`

The paths above are local. If another AI cannot access them, it must ask for the files it needs. It must not invent substitutes.

## Facts the narration may use

| Item | Shopper example | Merchant example |
|---|---|---|
| Request | `Show me order 4127.` | `Show me order 4127.` |
| Verified role | `shopper` | `merchant` |
| Verified user ID | `1` | `9002` |
| Store ID | Not required for the shopper tool span | `2` |
| Session ID | `637e81fd-e312-4232-9181-1562357fff34` | `b839204c-8cc0-45cc-921d-18e8995faa8e` |
| Root-span ID, not trace ID | `f9bb77c0cf092001` | `aa4cfa37b56010c9` |
| Prompt version | `b24e1d226ef2` | `b24e1d226ef2` |
| Tool order | `get_order` | `get_order` |
| Tool result | Order details returned | `permission_denied` |
| Final reply | Order 4127 is delivered; total $84 | Order is not accessible to this merchant |
| Request status | `completed` | `completed` |
| Entries in supplied span export | 6 | 6 |

The merchant denial reason is:

`role 'merchant' (user 9002) may not view order #4127`

The shopper's first model call recorded 867 input tokens and 61 output tokens. Its second recorded 1,030 input tokens and 84 output tokens. These are counts for two separate calls. Do not describe either as the total for the whole conversation.

The exports show permission values as the strings `"false"` and `"true"`. The application code sets Boolean values, but this export alone does not prove the stored field type. Narrate the access result without claiming the raw Boolean type was independently verified.

A denied tool call can belong to a successfully completed request. Here, `completed` means the agent finished handling the request. It does not mean access was granted.

Five live examples were reviewed in the tutorial: shopper order lookup, merchant denied lookup, Juniper return policy, an unrelated poem request, and refund eligibility for order 3980. The final video focuses on the two selected traces; it does not need to replay all five live requests.

## Visual and audio directions

- Use the real Langfuse interface and terminal. Prefer a 1920 × 1080 recording with text large enough to read.
- Prepare tabs before recording: shopper trace, merchant trace, first comparison trace, second comparison trace, and the terminal.
- Use one continuous recording. Navigate between tabs in real time. Do not insert generated screen images or splice together different runs.
- Keep the cursor near the field being discussed. Pause briefly after selecting an important field.
- Keep code views small and relevant. Do not scroll through whole files during narration.
- Use a calm, clear voice at about 120–130 words per minute. Leave time for clicking and reading. No music is needed.
- Do not show `.env`, API keys, bearer tokens, password fields, or terminal history containing them. Prepare a clean terminal before recording.
- For a rehearsal voice, pronounce `get_order` as “get order”, `gen_ai` as “gen A I”, and `cartwheel` as “cartwheel”. Keep the exact field names visible on screen.
- Leave long hashes on screen. The speaker can say “the original version” and “the changed version” rather than reading every character aloud.
- Captions are optional for a rehearsal. They must match the narration and must not cover the evidence.

## Scene plan

| Time | Screen action | What the viewer must see |
|---|---|---|
| 0:00–0:25 | Show the expanded shopper trace tree | One request, nested agent steps, two model calls, and one tool call |
| 0:25–1:05 | Switch to terminal, run the authentication test below; briefly show identity checks in `server/app.py` if time allows | Actual test name and result; identity comes from the stored database record |
| 1:05–2:05 | Open shopper root, first model, tool, final model, and final reply | Role and user ID, prompt version, tool input/result, token counts, reply |
| 2:05–2:55 | Open merchant root and follow its trace to the final reply | Merchant user 9002, store 2, denied result and reason, no returned order details |
| 2:55–4:00 | Show both verified prompt-comparison traces, then the restored prompt line | Same request/user/model, fresh histories, two different hashes, original wording restored |
| 4:00–4:40 | Run the span-count command; show the two corrected trace records | Regenerated count, six distinct entries, actual trace IDs and working permalinks |

Timing is a target, not proof of duration. Rehearse and measure the actual recording. Keep the finished take below five minutes.

## Commands to show

Run commands from the repository root. These commands are instructions for the student or for an approved rehearsal. They were not run while creating this brief.

### One authentication test

```bash
uv run pytest tests/test_observability.py::test_token_cannot_authorize_a_different_session -vv
```

This offline test creates two sessions and tries to use the first session's token with the second session. It expects rejection before the agent is built or run. Do not use the narration line “the test passed” unless the visible run passes. If it fails, stop the take, investigate, and record a new complete take after the issue is resolved.

### Regenerate one selected trace's span count

This counts the entries in the saved shopper trace export. It does not query the live service. Each entry represents a span or a specialized span such as a model generation. The checks identify the intended root span and reject duplicate entries.

```bash
uv run python -c 'import json; from pathlib import Path; rows=json.loads(Path("/Users/charliemac/.codex/attachments/531aa485-fe15-4c56-84ae-ae8d4afb3313/pasted-text.txt").read_text()); assert isinstance(rows, list); assert rows[0]["id"] == "f9bb77c0cf092001"; assert rows[0]["depth"] == 0; assert len({r["id"] for r in rows}) == len(rows); print("Shopper trace span count:", len(rows))'
```

Expected count from the supplied export: `6`. Use the actual command output in the recording. Do not replace it with typed or generated output.

The correct hierarchy is:

```text
cartwheel.session_message
└── Agent Workflow
    └── cartwheel-support.agent
        ├── model call: choose a tool
        ├── get_order
        └── model call: write the reply
```

## Voice script

Use this as a factual draft. The student should understand it and adapt it to their own voice. The voice-only copy is in `hw2-video-voice-script.txt`.

### Scene 1 — Purpose

“This is my Homework Two demonstration of Cartwheel. I added a checked session and a trace for each message. A trace records the whole request. A span records one step inside it. I will show an allowed lookup, a denied lookup, and how I track the prompt version.”

### Scene 2 — Identity and test

“First, I will run an access test. It checks that a pass issued for one conversation cannot open another conversation. The test passed. This test runs offline and makes no model call.

“The server checks the requested user and role against the database. It saves that identity with the session and issues a signed pass. Later messages use that saved identity. A claim inside the chat cannot change the user's role. This is a local course setup, not a complete production sign-in system.”

### Scene 3 — Allowed request

“Here is the request to show order four one two seven. The root span identifies shopper user one and records the prompt version. The workflow and agent entries group the steps below them.

“The first model call chooses the get order tool. The tool receives the order number and returns the order details. Access was allowed. The final model call turns those details into a reply: the order was delivered and its total was eighty-four dollars.

“The gen A I fields describe the model and tool work. The cartwheel fields describe the user and access decision. Token counts measure pieces of text read and written by the model. They are now visible for both model calls.”

### Scene 4 — Denied request

“Now I will follow the same request from merchant user nine thousand and two. The root span records the merchant identity. The tool span also records store two.

“The get order tool denies access and explains why: this merchant may not view order four one two seven. It returns no order details. The final reply explains the limit and offers help with the merchant's own store.

“The request completed successfully because the agent handled the denial. Completed does not mean that access was granted.”

### Scene 5 — Prompt comparison

Use the following paragraph for rehearsal of the already observed wording experiment. For the submission, resolve the Part F requirement above, then substitute the verified comparison wording and hashes. Do not silently describe this experiment as a comparison with the earlier HW1 prompt.

“These are the two prompt versions from the wording check. Both requests asked about a refund for order three nine eight zero, using shopper user one and the same model. Each began in a new session.

“The original prompt has the first code shown here. A temporary tone change produced the second code. This shows that changing the prompt changes its version code. It does not show that either prompt gives better answers. I restored the original wording afterward.”

Display the observed rehearsal hashes `b24e1d226ef2` and `0c8cc1a41e4b` only with their actual trace evidence. If redoing Part F with the earlier HW1 prompt, replace “wording check” with “prompt comparison” and “A temporary tone change” with “The earlier Homework One prompt”, and display that run's actual second hash.

### Scene 6 — Count and records

“Finally, I will count the spans again from the saved shopper trace export. The command reports six: the root, the workflow, the agent, two model calls, and one tool call.

“The trace record file contains the two examples I have shown, with their actual trace IDs, links, users, tool order, and completion status. This evidence lets someone follow each request from the verified identity through the tool result to the final reply.”

Only use the final paragraph after the IDs and links in `hw2-traces.json` are corrected and verified.

## Acceptance checklist for the video assistant

- [ ] The final recording is student-made, continuous, and no more than five minutes.
- [ ] One real authentication test is run and its actual result is shown.
- [ ] Both selected traces are read from root span to final reply.
- [ ] The explanation distinguishes verified server identity from claims in chat.
- [ ] The tool arguments, allowed result, denied result, and denial reason are visible.
- [ ] The two selected records use actual trace IDs, not span IDs, and working links.
- [ ] Both prompt hashes are shown in real trace evidence.
- [ ] The prompt comparison follows the handout's earlier-HW1-prompt requirement, or its exception is explicitly accepted by the instructor.
- [ ] The original prompt is restored; no unverified restoration claim is used.
- [ ] The span count is regenerated visibly and described as a saved-export count.
- [ ] No key, token, invented UI, fake test result, or unsupported assessment appears.
- [ ] The student reviews every spoken claim before recording or submission.

Do not mark Homework 2 complete merely because the script or rehearsal video is finished. The recording, corrected evidence, and required checks must actually be complete.
