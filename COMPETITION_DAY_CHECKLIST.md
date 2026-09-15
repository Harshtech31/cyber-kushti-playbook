# CYBER KUSHTI 2026 - COMPETITION-DAY MASTER CHECKLIST

> **921 Teams $\to$ Top 50 Advance**  
> **Key Deadlines:** 14:00 (Portal Access) | 17:00 (Repo Drop & Work Kickoff) | 22:30 (Freeze) | 22:45 (Portal Submit) | 23:00 (Hard Deadline)

---

## 1. Pre-Drop Readiness (13:30 - 14:00)

- [ ] Security tools environment verified (`source ~/.security-tools/venv/bin/activate`).
- [ ] Tooling availability verified: `semgrep`, `codeql`, `osv-scanner`, `gitleaks`, `trivy`, `docker`, `curl`, `jq`.
- [ ] LLM / AI access confirmed (API keys loaded or web interfaces ready).
- [ ] Shared team communication channel active (M1 Lead, M2 Code, M3 Dynamic).
- [ ] Working workspace cleaned; no residual files from past targets.
- [ ] Review [ROUND_1_CHEAT_SHEET.md](ROUND_1_CHEAT_SHEET.md) and [AI_PROMPTING_PLAYBOOK.md](AI_PROMPTING_PLAYBOOK.md).

---

## 2. Portal Onboarding & Pre-Fight Readiness (14:00 - 17:00)

*Portal access opens at 14:00. Target repo will be released at 17:00.*

- [ ] **14:00 - 14:30 | Portal Intake & Setup (M1)**:
  - [ ] Log in and verify portal credentials for all 3 team members.
  - [ ] Inspect the Portal Tracking System: Identify required input fields (Title, Severity, TP/FP dropdown, File/Line, Description, PoC, Fix).
  - [ ] Document portal attachment rules, character limits, and allowed formats (Markdown, PDF, ZIP).
  - [ ] Review rules of engagement, rate limits, and scoring penalties.
- [ ] **14:30 - 16:15 | Tooling Pipeline Dry-Run (M2 & M3)**:
  - [ ] Test Semgrep, Gitleaks, OSV-Scanner, and Trivy on a test repo.
  - [ ] Confirm Docker daemon is functioning (`docker ps`).
  - [ ] Test AI prompt templates ([AI_PROMPTING_PLAYBOOK.md](AI_PROMPTING_PLAYBOOK.md)) in your AI interface.
  - [ ] Set up local evidence structure: `scans/`, `evidence/`, `findings/`, `ai_outputs/`, `reports/`.
- [ ] **16:15 - 17:00 | Pre-Battle Alignment (All)**:
  - [ ] Assign roles for the 17:00 repo drop.
  - [ ] M1 prepares draft finding cards matching the portal tracking form.
  - [ ] Ready browser tabs and terminal sessions at 16:55.

---

## 3. Repo Release & Execution Window (17:00 - 22:30)

- [ ] **17:00 - 17:45 | Repo Ingest, Build & Discovery**:
  - [ ] M1: Clone repo into `target/`, record commit SHA (`git rev-parse HEAD`), inspect stack.
  - [ ] M3: Spin up Docker container (`docker compose up -d`) and confirm live listening ports (`ss -lntup`).
  - [ ] M2: Run automated scanners in parallel (`semgrep`, `gitleaks`, `trivy`, `osv-scanner`).
  - [ ] M1 & M2: Chunk routing and auth code into AI Prompts 1 & 2; store in `ai_outputs/`.
- [ ] **17:45 - 18:30 | Candidate Triage & Quick-FP Pruning**:
  - [ ] M1: Merge AI findings + tool alerts into canonical `SEC-XXX` IDs.
  - [ ] M2: Eliminate obvious AI hallucinations and dead code; mark as **FALSE POSITIVE** with code proof.
  - [ ] M3: Verify reachable routes against the live local application.
- [ ] **18:30 - 20:30 | Dual Static + Dynamic Deep Dive (Sprint 1)**:
  - [ ] Focus on Critical/High candidates (Authentication, Authorization/IDOR, Injection, SSRF).
  - [ ] M2 proves static path: Input $\to$ processing $\to$ missing server check $\to$ sink.
  - [ ] M3 proves dynamic runtime: curl request with payload $\to$ HTTP 200/leak/unauthorized state change $\to$ container log proof.
  - [ ] Challenge any candidate that fails runtime proof: Is it a False Positive?
- [ ] **19:30 - 20:45 | Business Logic & Chains (Sprint 2)**:
  - [ ] Test multi-step business logic (state transitions, payment bypass, mass assignment).
  - [ ] Build attack chains: e.g. Information Leak $\to$ Token Tampering $\to$ Privileged Admin Action.
  - [ ] Run "Devil's Advocate" checks on all High findings: Can a defender prove this doesn't work?
- [ ] **20:45 - 22:00 | Finding Report Drafting**:
  - [ ] Populate [FINDING_REPORT_TEMPLATE.md](FINDING_REPORT_TEMPLATE.md) for each canonical issue.
  - [ ] Ensure every finding has explicit `Verdict: TRUE POSITIVE` or `Verdict: FALSE POSITIVE`.
  - [ ] Verify each True Positive has: Static code location + Dynamic curl proof + Business impact + Root cause fix + Regression test.
  - [ ] Verify each False Positive has: Detailed technical justification debunking the scanner/AI claim.

---

## 4. Final Review & Buffer Submission (22:00 - 23:00)

- [ ] **22:00 - 22:30 | 3-Member Sign-Off Gate**:
  - [ ] M1 Sign-off: Business impact verified, severity justified, duplicates resolved.
  - [ ] M2 Sign-off: Source code line numbers verified, patches accurate.
  - [ ] M3 Sign-off: Reproducible curl commands verified, evidence screenshots/logs attached.
- [ ] **22:30 | Content Freeze**:
  - [ ] Absolute freeze on editing findings. No new candidates allowed.
- [ ] **22:30 - 22:45 | Package & Sanitize**:
  - [ ] Redact sensitive passwords/keys in proof; replace with safe placeholders (`<REDACTED_API_KEY>`).
  - [ ] Verify file naming and report format comply with organizer instructions.
  - [ ] Build submission archive (`zip` / `tar.gz` / `pdf`).
- [ ] **22:45 | Submission Dispatch**:
  - [ ] Submit package 15 minutes before 23:00 deadline.
  - [ ] Verify upload confirmation page, submission ID, and timestamp.
  - [ ] Store local backup copy of exact submitted archive with SHA256 checksum.


