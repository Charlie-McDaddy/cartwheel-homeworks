# AI production brief: create the complete Homework 1 video

## Your task

Create the finished video, including the explanation, AI narration, screen operation, and one continuous screen recording. Do not stop at a storyboard or ask the student to narrate or operate the recorder.

The user explicitly requests full AI production. This overrides the earlier brief's student-recording workflow. Preserve the student's recorded assessments. Do not invent personal experiences, new judgments, conversations, or results.

Target duration: 4 minutes 30 seconds. Hard limit: 5 minutes.
Output: a playable video with readable evidence and clear narration.
Use a neutral synthetic voice. Identify the video as AI-narrated. Do not clone the student's voice or imply the student personally recorded it.

The assignment asks for a continuous screen video with the student's explanation. AI production is the user's chosen format; acceptance of that format by the course has not been verified. State this limitation in the handoff. Do not claim that the recording meets every submission rule merely because it covers the required content.

## 1. Load the evidence

Work from:

```text
/Users/charliemac/Desktop/Coding/cartwheel-homeworks
```

Read these sources before writing narration or building the screen views:

| File | Purpose |
| --- | --- |
| `AGENTS.md`, `homework/module-1/AGENTS.md` | Repository rules; apply the user's explicit AI-production request above |
| `homework/module-1/hw1.md` | Required video content |
| `hw1-video-checklist.md` | Existing checklist; its student-recording direction is superseded for this task |
| `SPEC.md` | AUTH-1, ESC-1, ESC-2 |
| `facts.yaml` | Policy values |
| `hw1-session.jsonl` | Ten saved conversations and student assessments |
| `hw1-prompt-comparison.json` | Matched email-change experiment |
| `agent/agent.py` | Actual prompt edit and registered tools |
| `agent/tools.py` | Required tools and added refund eligibility tool |
| `.codex/hw1-refund4455-session.jsonl` | First refund turn |
| `.codex/hw1-refund4455-followup.jsonl` | Refund follow-up and exact tool results |

Parse JSON and JSONL with a JSON parser. Select conversation records by role, user ID, and request. The same order appears in different role tests.

The root record for order 4455 shortens the two-turn exchange. Use the two original captures for exact dialogue. Do not display the shortened record as a verbatim transcript. If the original captures are unavailable, request the missing evidence or label the root record as a summary. Never invent the omitted dialogue.

Historical results: ten conversation records, six focused HW1 tests passed, and another 39 new-tool/regression tests passed. Verify the current values. The recorded terminal scene must show a new actual test run and an actual count calculation.

## 2. Build the evidence views

Create a local presentation viewer or prepare editor views with these pages:

1. Title and provenance.
2. Authorized shopper lookup for order 4127.
3. Merchant permission denial for order 4127.
4. The two-turn refund request for order 4455.
5. Email-change before response.
6. Exact account-change prompt edit.
7. Email-change after response and tool result.
8. Terminal for tests and record count.

A local viewer is a display of saved evidence, not a new chat application. Populate it directly from the source files. Preserve exact source text. Visually separate requests, tool calls, results, responses, and assessments.

Label all chat pages:

```text
Saved live model run — recorded evidence
```

Label the title and include a small persistent footer:

```text
AI-narrated demonstration • Cartwheel demo data
```

Do not add typing animations, fake loading states, fake terminal output, or anything that presents historical chats as new live responses.

Use 1920 × 1080 at 30 frames per second where supported. Use large text, roughly 24–30 pixels for main content. Use high contrast, simple layouts, and enough space to read tool results. Split long content across deliberate screen views instead of shrinking it. Use no music, decorative animation, or stock footage.

Keep secrets and unrelated windows off screen. Never open `.env` during recording.

## 3. Write and generate the narration

Use the narration below as a factual starting script. Confirm all claims against the files. Adapt it to the actual test and count results. Use approximately 450–550 spoken words at a calm pace. Do not add first-person student claims such as “I learned” or “I decided.” Attribute assessments to the saved student judgments.

### Opening: 0:00–0:15

Show the title and provenance label.

Suggested narration:

“ This AI-narrated demonstration shows the completed Cartwheel Homework 1 work. Cartwheel is a shop support agent. The conversations shown here are saved real model runs. The tests at the end will run during this recording. ”

### Authorized request: 0:15–0:50

Show shopper user 1 requesting order 4127. Highlight `get_order`, `ok: true`, and the order details.

Suggested narration:

“ First, shopper user one asks to see order 4127. The order tool checks whether this shopper may see it. The tool returns success. The agent displays the Blue Heron Ceramics order, its 84-dollar total, and its delivered status. The student marked this result as meeting the expectation. ”

### Permission denial: 0:50–1:20

Show merchant user 9002, store 2, requesting the same order. Highlight `permission_denied` and the refusal.

Suggested narration:

“ Now a merchant from store two asks for the same order. This order belongs to another store. The tool returns permission denied. The agent does not display the private order details. This shows why access checks belong in the tool code. The model's wording alone does not protect the data. ”

### Refund above the threshold: 1:20–2:10

Show the two original turns in order. Highlight the initial `get_order`, the follow-up request, `issue_refund`, `queued_for_approval`, and `escalate_to_human`.

Suggested narration:

“ Order 4455 has a total of 240 dollars. The automatic refund threshold is 100 dollars. In the first turn, the agent checks the order and asks for more information. The shopper then asks for the full amount and a human referral. The refund tool queues the request for human approval. A separate tool creates a demo support ticket. The refund was not paid automatically. The saved capture also notes that the model supplied a refund reason that the user had not given. The approval result does not mean every part of the exchange was correct. ”

### Prompt investigation: 2:10–3:25

Show ESC-2, the exact before response, the added instruction, and the after result.

Exact added instruction:

```text
For account changes of any kind, including email address changes, call
escalate_to_human to create a support ticket.
```

Suggested narration:

“ The next test concerns an email address change. Rule ESC-2 says account changes must go to a human. Before the edit, the agent directed the shopper to account settings. It called no tools and created no ticket. The student marked that as a failure. The prompt was then given this explicit account-change instruction. The same request was repeated with the same role, tools, and starting data in a fresh chat. This time, the agent called the human-referral tool. The tool reported success and created demo ticket 151. The student marked the referral requirement as passed. This is evidence that the edit helped in this test. It does not prove every future request will work. ”

Keep the following limits visible in a short note on the experiment page:

- The after response did not cite a policy document for the stated follow-up time.
- The pass assessment concerns ESC-2.
- The dragon-poem failure remains unresolved by this account-change edit.

### Test run: 3:25–4:05

Switch to the actual terminal. Run the focused test command. Wait for its real completion.

Suggested narration before execution:

“ These are offline code tests. They do not call a live model. The option shown here makes unfinished homework functions fail instead of hiding them as expected failures. ”

After execution, read the observed summary. Do not use prerecorded claims of success unless the actual run matches. Use a short silent hold if needed while the command runs.

### Count and close: 4:05–4:30

Run the record-count command. Show its actual output.

Suggested narration, conditional on a verified count of ten:

“ The file contains ten saved conversations across the three roles. The before-and-after prompt evidence is stored separately. The extra refund eligibility tool also has offline tests. It checks access and eligibility without issuing a refund. All tickets shown here belong to local demo data. No real support handoff is claimed. ”

If the count differs, use the actual value and explain the discrepancy before making the final take.

## 4. Execute the terminal scenes

Set the terminal directory before recording:

```bash
cd /Users/charliemac/Desktop/Coding/cartwheel-homeworks
```

During the test scene, run:

```bash
uv run pytest --runxfail tests/test_hw_holes.py -k hw1
```

If `uv` cannot run but the existing environment works, use:

```bash
.venv/bin/python -m pytest --runxfail tests/test_hw_holes.py -k hw1
```

During the count scene, run:

```bash
uv run python -c 'import json; from pathlib import Path; rows = [json.loads(line) for line in Path("hw1-session.jsonl").read_text().splitlines() if line.strip()]; print(len(rows))'
```

The same `.venv/bin/python` fallback is allowed for counting.

Never substitute a hard-coded number, animated console, screenshot of an old test, or generated test summary for these live terminal actions.

Use the saved chats by default. Do not reset the main database or rerun refunds to produce a screen. If fresh model calls become necessary, use temporary demo data, follow the repository workflow, and capture the actual outcome.

## 5. Make one continuous recording

Inventory the available screen recorder, playback, text-to-speech, and media tools. Use supported tools and documented APIs. The user has requested production; proceed with the available capabilities without asking them to narrate.

Generate the narration audio first. Rehearse the screen sequence and timing. Use silent gaps for terminal completion rather than speaking over an unknown result. If needed, prepare short alternate result lines, but choose one only after the real result is known.

Start one screen capture with audio capture enabled. Play the AI narration through the captured audio source while operating the prepared views and terminal. Keep the capture running from the title to the closing screen. The AI operator controls the scene changes and command execution.

Do not assemble the final video from separate screen clips. Do not splice in terminal output. Do not speed up, cut away from, or hide failed commands. If the take exceeds five minutes or a command fails, resolve the issue and record a new full take.

If system audio capture is unavailable, capture one uninterrupted screen take and mix the narration onto that same uncut take afterward. Preserve screen timing. Do not describe the narration as a live microphone recording. Keep the AI-narrated label visible.

If no actual screen-recording capability exists, report that specific limitation. Do not quietly replace the requested continuous screen capture with a synthetic slideshow. Prepare any unaffected assets and state what capability is needed to finish.

## 6. Verify the completed media

Inspect the output using available media metadata and playback tools. Verify:

- Duration is at most 300 seconds.
- The screen footage is one continuous take.
- All required scenes appear in order.
- The real test finishes on screen.
- The actual count calculation is shown.
- Narration matches the visible evidence and does not run ahead of results.
- Text and code are readable at normal playback size.
- Audio is clear, audible, and free of clipping.
- The video discloses AI narration and saved chat evidence.
- No secret or unrelated personal content is visible.

Check the full audio and all scene transitions. Metadata alone cannot establish continuity or factual accuracy. Do not mark checks passed if you could not inspect them.

The refund ticket and email ticket both use ID 151 in separate temporary databases. Do not imply they are the same ticket. The new eligibility tool has offline verification; no live chat verification is established by the current evidence.

## Output and handoff

Create `hw1-demo.mp4` with H.264 video and AAC audio if available. Use 1080p and 30 fps where supported. If the recorder uses another format, convert only if needed for compatibility. Preserve the continuous screen sequence.

Keep large media outside Git unless the user asks otherwise. Do not publish or submit the video without an instruction to do so.

Deliver:

1. The finished playable video and its absolute path.
2. The narration transcript.
3. A short verification note with duration, actual test/count results, and any limitation.

State that AI-produced submission acceptance has not been verified. Do not mark the student's course submission complete.

The task is complete when the full narrated video is produced and checked, or when a specific unavailable production capability is clearly reported. A storyboard alone is not the requested deliverable.
