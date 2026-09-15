# CYBER KUSHTI 2026 - ROUND 1 AKHADA CHEAT SHEET

> **921 TEAMS $\to$ 50 ADVANCE (Top 5.4% Cutoff)**  
> **OFFICIAL PLATFORM:** [http://hackathon.nsd.org.in/login](http://hackathon.nsd.org.in/login)  
> **CONFIRMED SCORING FORMULA:**  
> $$\text{Total Score} = \text{Classification Score} + \text{Justification Score} + \text{Bonus} - \text{Penalty}$$  
> **THE GOLDEN RULE:** This is a **Precision & Accuracy** competition, NOT a volume contest. Getting 10 out of 10 findings correct with solid reasoning will beat a team that submits 30 findings with 10 wrong calls due to heavy penalties!

---

## The Master Timetable

| Clock | Phase | Action on http://hackathon.nsd.org.in |
| :--- | :--- | :--- |
| **14:00 – 17:00** | **Portal Setup & Key Prep** | Log into portal, confirm team members, check stage status, **prepare AI API keys** (Anthropic Claude Sonnet or OpenAI). |
| **17:00 – 17:15** | **Scan Trigger** | Repo allocated! Select **Anthropic (Claude Sonnet)** (or OpenAI), paste API Key, and click **Run Scan**. |
| **17:15 – 17:45** | **Live Scan Ingestion** | Monitor real-time scan logs. Findings populate the "Scan findings" table automatically. |
| **17:45 – 20:30** | **Precision Triage (TP vs FP)** | Open each finding: Select `TRUE_POSITIVE` or `FALSE_POSITIVE` MCQ option, write clear reasoning, and click Save. |
| **20:30 – 21:30** | **Deep Justification Audit** | Polish every justification to maximize `Justification Score` and eliminate false calls to avoid `Penalty`. |
| **21:30 – 22:30** | **Review & Audit** | Verify `Answered: All · Unanswered: 0`. 3-Member Peer Review sign-off. |
| **22:30 – 22:45** | **Lock & Submit** | Go to Qualifier Submission page $\to$ click **"Confirm submission"** (locks entry before 23:00). |
| **22:45 – 23:00** | **Verification** | Confirm status displays `SUBMITTED v1` and verify confirmation. |

---

## How to Maximize the Scoring Formula

1. **Classification Score (MCQ Call)**:
   - Select either `TRUE_POSITIVE` or `FALSE_POSITIVE`.
   - Never guess! A wrong call triggers the `Penalty` deduction.
2. **Justification Score (Your Reasoning)**:
   - Evaluated by judges on technical correctness.
   - **For True Positive**: State the source parameter, why the check is missing, and the sensitive sink reached.
   - **For False Positive**: State the exact protective control (e.g. ORM parameterized binding, framework auto-escaping, unreachable dead code, non-attacker input).
3. **Zero-Penalty Strategy**:
   - High-precision models (like Claude Sonnet) return fewer hallucinations, making it dramatically easier to achieve 100% accuracy and avoid penalties.

---

## The Platform Form Fields (Exact Schema)

When reviewing each finding in the portal (`/api/vulnerabilities/{id}/response`), you must fill in:

1. **Classification Dropdown**:
   - `TRUE_POSITIVE`
   - `FALSE_POSITIVE`
2. **Why did you classify this finding this way? (Justification)**:
   - For TP: Clear 2-3 sentence root-cause summary explaining why input reaches sink without authorization/sanitization.
   - For FP: Exact technical debunking (e.g. framework auto-escaping, ORM parameterization, dead code, non-attacker input).
3. **Optional Evidence (evidence_text)**:
   - Code line citations, safe curl reproduction request/response, or ripgrep proof.

---

## Supported AI Providers & Models in the Portal

| Provider | Supported Models | API Key Format |
| :--- | :--- | :--- |
| **Google** | `gemini-3.1-pro-preview`, `gemini-3-flash-preview`, `gemini-2.5-pro` | Google AI Studio Key (Get free from [aistudio.google.com](https://aistudio.google.com/)) |
| **Anthropic** | `claude-sonnet-5`, `claude-opus-5`, `claude-haiku-4-5-20251001` | Starts with `sk-ant-...` |
| **OpenAI** | `gpt-5.6-sol`, `gpt-5.6`, `gpt-5` | Starts with `sk-...` |
| **Qwen** | `qwen-max`, `qwen-plus`, `qwen-turbo` | DashScope Key |

*Repo drops at 17:00 sharp. Fire parallel discovery pipelines immediately.*

1. **Intake & Fingerprint (M1 - 17:00 - 17:10)**:
   - `git clone <repo-url> target/ && cd target && git rev-parse HEAD > ../target_commit.txt`.
   - Inspect tech stack (`package.json`, `requirements.txt`, `pom.xml`, `Dockerfile`, `docker-compose.yml`).
2. **Build Local Containerized Target (M3 - 17:10 - 17:45)**:
   - Run `docker compose up -d` or start local server. Verify listening ports (`ss -lntup`), health endpoints, and seed credentials.
3. **Run Multi-Tool Scanners in Parallel (M2 - 17:10 - 17:45)**:
   - Fire Semgrep, Gitleaks, OSV-Scanner, and Trivy in parallel (see [COMMAND_CHEAT_SHEET.md](COMMAND_CHEAT_SHEET.md)).
4. **Feed Critical Code to AI Prompts (M1 & M2 - 17:15 - 17:45)**:
   - Chunk routing, auth middleware, and controllers into AI Prompts 1 & 2 ([AI_PROMPTING_PLAYBOOK.md](AI_PROMPTING_PLAYBOOK.md)). Save outputs in `ai_outputs/`.

---

## Phase 2: Triage & Quick-FP Pruning (17:45 - 18:30)

*Goal: Merge tool alerts and AI outputs into 15–20 high-value canonical candidates.*

- **M1**: Consolidate scanner alerts and AI findings into canonical `SEC-XXX` IDs. Align them with the portal tracking categories.
- **M2**: Prune obvious AI hallucinations (non-existent files, unrouted functions, dead code) and mark as **FALSE POSITIVE** with code proof.
- **M3**: Confirm active, reachable HTTP routes against the running local Docker instance.

---

## Phase 3: Dual Static + Dynamic Verification (18:30 - 20:30)

*Goal: Prove True Positives with 2-point evidence (Source Path + Runtime Behavior).*

### The Candidate Verification Test

```text
[Candidate Alert] (AI / SAST / SCA)
       │
       ▼
1. Is Input Attacker-Controlled? ──(No)──> [FALSE POSITIVE] (Record reason)
       │ (Yes)
       ▼
2. Does Code Trace from Source to Sink? ──(Sanitized/Blocked)──> [FALSE POSITIVE]
       │ (Unsanitized)
       ▼
3. Can Runtime Request Reach It? ──(Unexposed/Dead)──> [FALSE POSITIVE / LOW]
       │ (Reachable)
       ▼
4. Does Dynamic Execution Prove Impact?
       ├── (Yes: HTTP 200/500/State Change/Data Leak) ──> [TRUE POSITIVE - CONFIRMED]
       └── (No: Framework blocked at runtime) ──> [FALSE POSITIVE / PARTIAL]
```

- **M2 Workflow (Static Source Trace)**:
  - Trace parameter from entry point (controller/route) $\to$ service $\to$ data access $\to$ sink.
  - Check whether server-side authorization checks are performed before the sink.
  - Document file path and exact lines in the finding.
- **M3 Workflow (Dynamic Runtime Proof)**:
  - Craft safe, non-destructive curl / HTTP request.
  - Capture request and response headers/body showing the policy violation.
  - Capture container/app logs confirming execution at the sink.

---

## Phase 4: Attack Chains & Deep Business Logic (20:30 - 21:30)

*Goal: Find what AI and scanners missed—chained exploits and multi-step logic bypasses.*

- **IDOR / BOLA / Tenant Leaks**: Can User A access User B's object ID directly?
- **State Machine Tampering**: Can checkout/approval skip payment or verification steps?
- **Mass Assignment**: Can client-supplied JSON overwrite `role: "admin"` or `verified: true`?
- **Chained Impact**: Link `Low` info leak + `Medium` auth flaw into a `Critical` finding.

---

## Phase 5: Portal Entry, Report Compilation & Peer Review (21:30 - 22:30)

*Goal: Polish every report and enter findings into the competition portal tracking system.*

- **Enter into Portal Tracking System (M1)**:
  - Populate portal fields directly using [FINDING_REPORT_TEMPLATE.md](FINDING_REPORT_TEMPLATE.md).
  - Explicitly mark each entry as `TRUE POSITIVE` or `FALSE POSITIVE`.
- **Finding Quality Standard**:
  - Confirmed **True Positives (TP)**: Static source-to-sink path (file + lines), dynamic curl command + HTTP response, container log proof, root cause fix diff, and regression test.
  - Confirmed **False Positives (FP)**: Technical debunking showing why the scanner/AI flagged it and why framework auto-escaping, ORM parameterization, or dead code prevents exploitation.
- **The 3-Member Sign-off Gate**:
  - M1 checks: Portal form fields, severity, business impact, clear formatting.
  - M2 checks: Static code accuracy, root cause explanation, patch diffs.
  - M3 checks: Dynamic reproducibility, evidence validity, screenshot/log attachments.

---

## Phase 6: Submission Freeze & Portal Verification (22:30 - 23:00)

- **22:30**: Absolute content freeze. No new findings or portal edits.
- **22:30 - 22:45**: Bundle reports, sanitize secrets, verify portal attachments, confirm submission requirements.
- **22:45**: Final submission in the portal (15-minute safety buffer against portal server slowdowns).
- **22:45 - 23:00**: Verify portal submission status, save confirmation screenshot, and archive submission package.

---

## Quick Rules of Engagement

1. **AI output is an unverified lead**: AI hallucinates context and flags safe sanitizers as vulnerabilities. Always verify against source.
2. **False Positives are scoring gold**: Accurately debunking false alerts proves human expertise over automated script-kiddies.
3. **Dual proof is mandatory**: Code path alone is theoretical; dynamic proof alone lacks root cause. Combine both for high judge scores.
4. **No destructive tests**: Never drop tables, crash containers, or run automated denial-of-service payloads.


