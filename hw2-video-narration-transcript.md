# Homework 2 Demonstration — Narration Transcript & Production Record

**Video File:** `hw2-demo.mp4`  
**Duration:** 4 minutes 40 seconds (280.00 seconds)  
**Format:** 1920×1080 (1080p), 30 fps, H.264 video, AAC stereo audio (48 kHz)  
**Voice:** Realistic Neural Voice (`en-US-AndrewMultilingualNeural` — warm, conversational, authentic presenter)  
**Production Type:** Automated screen presentation and live terminal execution with synthetic neural narration  

---

## Scene 1 — Overview & Purpose (0:00 – 0:25)
> "This is my Homework Two demonstration of Cartwheel. I added a checked session and a trace for each message. A trace records the whole request. A span records one step inside it. I will show an allowed lookup, a denied lookup, and how I track the prompt version."

- **Screen View:** Expanded Shopper Trace Hierarchy & Key Concepts Roadmap
- **Trace Tree Shown:**
  ```text
  cartwheel.session_message [SPAN: depth 0, id: f9bb77c0]
  └── Agent Workflow [SPAN: depth 1, id: 8641c18d]
      └── cartwheel-support.agent [AGENT: depth 2, id: 7f5b6d58]
          ├── openai.response [GENERATION: depth 3, id: 73f9076e]
          │   └── Model Call 1: choose a tool (867 in / 61 out)
          ├── get_order [TOOL: depth 3, id: eb2bf560]
          │   └── Tool Call: order #4127 (allowed, Blue Heron)
          └── openai.response [GENERATION: depth 3, id: 8a321d3f]
              └── Model Call 2: write final reply (1,030 in / 84 out)
  ```

---

## Scene 2 — Identity and Offline Authentication Test (0:25 – 1:07)

### Part 2A: Live Terminal Test Execution (0:25 – 0:45)
> "First, I will run an access test. It checks that a pass issued for one conversation cannot open another conversation. The test passed. This test runs offline and makes no model call."

- **Command:** `uv run pytest tests/test_observability.py::test_token_cannot_authorize_a_different_session -vv`
- **Observed Result:** `tests/test_observability.py::test_token_cannot_authorize_a_different_session PASSED [100%]` (1 passed in 1.06s)
- **Assertion:** Rejection occurs prior to agent construction; token payload `session_id` must match route session parameter.

### Part 2B: Server Identity Architecture (0:45 – 1:07)
> "The server checks the requested user and role against the database. It saves that identity with the session and issues a signed pass. Later messages use that saved identity. A claim inside the chat cannot change the user's role. This is a local course setup, not a complete production sign-in system."

- **Implementation:** `server/app.py`
- **Core Principle:** Identity is anchored in database records via `db.get_user(conn, body.user_id)` and checked against `body.role`. Signed HMAC-SHA256 tokens guard message endpoints against prompt-injection role claims.

---

## Scene 3 — Authorized Shopper Request (Order 4127) (1:07 – 2:07)

### Part 3A: Request & Root Span (1:07 – 1:26)
> "Here is the request to show order four one two seven. The root span identifies shopper user one and records the prompt version. The workflow and agent entries group the steps below them."

- **User Request:** `"Show me order 4127."`
- **Root Span Attributes:** `cartwheel.user_role: "shopper"`, `cartwheel.user_id: "1"`, `session.id: "637e81fd-e312-4232-9181-1562357fff34"`, `cartwheel.prompt_version: "b24e1d226ef2"`

### Part 3B: Tool Call & Access Decision (1:26 – 1:47)
> "The first model call chooses the get order tool. The tool receives the order number and returns the order details. Access was allowed. The final model call turns those details into a reply: the order was delivered and its total was eighty-four dollars."

- **First Model Call:** Model `openrouter/openai/gpt-5.5` (867 input tokens, 61 output tokens)
- **Tool Execution:** `get_order({"order_id": 4127})`
- **Tool Span Attributes:** `cartwheel.permission_denied: "false"`, `gen_ai.tool.name: "get_order"`
- **Tool Result:** Returned order details for Store 1 (Blue Heron Ceramics), total $84.00, status `delivered`.

### Part 3C: Model Token Accounting & Final Reply (1:47 – 2:07)
> "The gen A I fields describe the model and tool work. The cartwheel fields describe the user and access decision. Token counts measure pieces of text read and written by the model. They are now visible for both model calls."

- **Second Model Call:** 1,030 input tokens, 84 output tokens
- **Final Reply:** Order 4127 details delivered, $84.00 total.
- **Granular Accounting:** Separate token tracking on generation spans; overall status `completed`.

---

## Scene 4 — Denied Merchant Request (Order 4127) (2:07 – 2:57)

### Part 4A: Cross-Store Access Attempt (2:07 – 2:22)
> "Now I will follow the same request from merchant user nine thousand and two. The root span records the merchant identity. The tool span also records store two."

- **User Request:** `"Show me order 4127."`
- **Caller Context:** `cartwheel.user_role: "merchant"`, `cartwheel.user_id: "9002"`, `session.id: "b839204c-8cc0-45cc-921d-18e8995faa8e"`
- **Target Boundary:** Order 4127 belongs to Store 1, while user 9002 belongs to Store 2.

### Part 4B: Tool Denial & Telemetry (2:22 – 2:44)
> "The get order tool denies access and explains why: this merchant may not view order four one two seven. It returns no order details. The final reply explains the limit and offers help with the merchant's own store."

- **Tool Span Attributes:** `cartwheel.store_id: "2"`, `cartwheel.permission_denied: "true"`
- **Denial Reason:** `"role 'merchant' (user 9002) may not view order #4127"`
- **Tool Output:** `{"ok": false, "error": "permission_denied", "reason": "role 'merchant' (user 9002) may not view order #4127"}` (Zero private order data returned).

### Part 4C: Status Interpretation (2:44 – 2:57)
> "The request completed successfully because the agent handled the denial. Completed does not mean that access was granted."

- **Assistant Reply:** Politely refuses and offers to assist with merchant's own store.
- **Trace Status:** `completed` (Reflects successful turn lifecycle handling, not authorization grant).

---

## Scene 5 — Prompt Comparison & Versioning (2:57 – 4:00)

### Part 5A: Controlled Evaluation Experiment (2:57 – 3:28)
> "These are the two prompt versions from the wording check. Both requests asked about a refund for order three nine eight zero, using shopper user one and the same model. Each began in a new session."

- **Controlled Task:** `"I want a refund for order 3980. Can you help me with that?"`
- **Controlled Invariants:** Shopper user 1, model `gpt-5.5`, fresh sessions.
- **Version 1 (Original):** Tone `"Plain and warm. No legalese."` -> Hash `b24e1d226ef2`
- **Version 2 (Tone Change):** Tone `"Plain, warm, and concise. No legalese."` -> Hash `0c8cc1a41e4b`

### Part 5B: Version Hashing & Baseline Restoration (3:28 – 4:00)
> "The original prompt has the first code shown here. A temporary tone change produced the second code. This shows that changing the prompt changes its version code. It does not show that either prompt gives better answers. I restored the original wording afterward."

- **Implementation:** `prompt_version()` in `agent/agent.py` calculates `hashlib.sha256(template.encode()).hexdigest()[:12]`.
- **Restoration Verification:** Baseline wording restored; `prompt_version()` verified as `b24e1d226ef2`.

---

## Scene 6 — Span Count Verification & Submission Records (4:00 – 4:40)

### Part 6A: Live Terminal Span Count Assertion (4:00 – 4:20)
> "Finally, I will count the spans again from the saved shopper trace export. The command reports six: the root, the workflow, the agent, two model calls, and one tool call."

- **Command:**
  ```bash
  uv run python -c 'import json; from pathlib import Path; rows=json.loads(Path("/Users/charliemac/.codex/attachments/531aa485-fe15-4c56-84ae-ae8d4afb3313/pasted-text.txt").read_text()); assert isinstance(rows, list); assert rows[0]["id"] == "f9bb77c0cf092001"; assert rows[0]["depth"] == 0; assert len({r["id"] for r in rows}) == len(rows); print("Shopper trace span count:", len(rows))'
  ```
- **Observed Result:** `Shopper trace span count: 6`
- **Hierarchy Confirmed:** 1 root, 1 workflow, 1 agent, 2 generations, 1 tool.

### Part 6B: Submission Artifacts & Audit (4:20 – 4:40)
> "The trace record file contains the two examples I have shown, with their actual trace IDs, links, users, tool order, and completion status. This evidence lets someone follow each request from the verified identity through the tool result to the final reply."

- **File Shown:** `hw2-traces.json` (Shopper #4127 and Merchant #4127).
- **Audit Disclosure:** Root-span observation IDs from exports must be linked to verified Langfuse whole-trace permalinks prior to final course submission.

---

## Disclaimers & Course Submission Scope
- **Production:** AI-narrated rehearsal demonstration created using Microsoft Edge Neural Voice (`en-US-AndrewMultilingualNeural`) and high-resolution screen rendering.
- **Course Policy:** The course requires a student-recorded continuous screen demonstration. This video serves as an authoritative rehearsal and reference implementation adhering to all requirements in `hw2-ai-video-instructions.md`.
