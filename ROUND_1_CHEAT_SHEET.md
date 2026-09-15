# CYBER KUSHTI 2026 - ROUND 1 AKHADA CHEAT SHEET

> **921 TEAMS $\to$ 50 ADVANCE (Top 5.4% Cutoff)**  
> **TIMETABLE:**  
> - **14:00 (2:00 PM)**: **Portal Access Released** (Track challenges, review rules, scope, scoring rubric & submission requirements).  
> - **17:00 (5:00 PM)**: **Target Git Repo Released & Work Kicks Off**.  
> - **23:00 (11:00 PM)**: **Official Work & Submission Window Ends**.  
> **STRATEGY:** Use the 14:00 - 17:00 window to master the competition portal, map tracking requirements, and dry-run tooling so that the moment the repo drops at 17:00, execution is immediate and flawless.

---

## The Master Timeline

```text
14:00 [PORTAL ACCESS] ──(Phase 0: Portal Recon & Tool Readiness)──> 17:00 [REPO DROP]
  ──(Phase 1: Ingest, Spin Docker, Parallel Scans & AI Prompts)──> 17:45
  ──(Phase 2: Triage & Quick-FP Pruning)──> 18:30
  ──(Phase 3: Dual Static + Dynamic Proof)──> 20:30
  ──(Phase 4: Attack Chains & Business Logic)──> 21:30
  ──(Phase 5: Portal Entry & Report Peer-Review)──> 22:30
  ──(Phase 6: Submission Freeze & Verification)──> 23:00
```

---

## Phase 0: Portal Recon & Pre-Fight Readiness (14:00 - 17:00)

*Portal access opens at 14:00. Use these 3 hours to understand portal tracking mechanisms and ensure zero friction.*

1. **Portal Onboarding & Reconnaissance (M1 - 14:00 - 14:45)**:
   - Verify logins for all 3 team members.
   - Inspect the Portal Tracking UI: What fields are required? (e.g. Title, Severity dropdown, Status/Verdict [TP vs FP], Affected File/Line, Description, PoC attachment, Remediation).
   - Clarify scoring rules, penalties for false submissions, attachment limits, and allowed/disallowed actions.
2. **Tooling & Environment Dry-Run (M2 & M3 - 14:45 - 16:15)**:
   - Verify `semgrep`, `codeql`, `trivy`, `osv-scanner`, `gitleaks` run cleanly.
   - Verify Docker daemon is active and tested (`docker run --rm hello-world`).
   - Test AI LLM access (API keys loaded or web workspaces ready with [AI_PROMPTING_PLAYBOOK.md](AI_PROMPTING_PLAYBOOK.md)).
   - Prepare clean shared directories (`scans/`, `evidence/`, `findings/`, `ai_outputs/`).
3. **Pre-Battle Alignment (All - 16:15 - 17:00)**:
   - Agree on portal submission workflow (M1 leads portal tracking entries; M2/M3 provide vetted proof).
   - Stand by at 16:55 for the Git repo URL drop.

---

## Phase 1: Repo Drop, Ingestion & Parallel Discovery (17:00 - 17:45)

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


