# CYBER KUSHTI 2026 - TEAM MASTER PLAYBOOK

> **AUTOMATION FINDS SIGNAL. HUMANS DETERMINE TRUTH. DYNAMIC TESTING PROVES IMPACT. ATTACK CHAINS DETERMINE PRIORITY. CLEAR EVIDENCE WINS THE ARGUMENT.**

This is the operating manual for exactly three people. It applies only to the controlled environments supplied by the organisers. Never test a live system, public service, or third party.

## 1. Competition Overview

**Verified source:** [PIB announcement, Release ID 2300120](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2300120&reg=6&lang=1), published 16 August 2026.

| Fact | Publicly stated / Confirmed |
| --- | --- |
| Name | CYBER KUSHTI 2026: National Cybersecurity & AI Hackathon |
| Organisers | NIELIT/MeitY with ISAC Foundation; CERT-In is Knowledge Partner |
| Competition Pool | **921 Registered Teams** across India |
| Round 1 Advancement | **Top 50 Teams advance to Round 2 (Top 5.4% Selection Rate)** |
| Team size | Three; students and independent researchers (M1, M2, M3) |
| Core task | Given a Git repository containing vulnerabilities: Use AI prompts + multi-tool security scanners to discover flaws, conduct dual static and dynamic analysis, and classify every candidate as True Positive or False Positive with proof |
| Shared material | Git repository, source code, dependency manifests, Docker configs, application logs |
| AI tools | **Mandatory / Explicitly permitted**; utilized for automated auditing, surface mapping, and hypothesis generation |
| Safety boundary | Controlled local/containerized target environments only; no live, third-party, or public infrastructure |

The competition rewards judgment, not finding volume. In a 921-team field, submitting unverified scanner dumps or hallucinated AI claims will lead to instant disqualification. A defensible, technically proven False Positive rejection carries as much weight as a confirmed True Positive.

## 2. Rules / Confirmed Schedule & Constraints

### Confirmed rounds & Schedule

| Round | Name | Date / format | Timetable / Outcome |
| --- | --- | --- | --- |
| **1** | **Akhada** | **Online, 15 September 2026** | **Portal Access: 14:00 (2:00 PM)**<br>**Repo Release & Kickoff: 17:00 (5:00 PM)**<br>**Submission Deadline: 23:00 (11:00 PM)**<br>*Outcome: Top 50 teams advance (5.4%)* |
| 2 | Dangal | Online, 24 September 2026 | 10 finalist teams selected |
| 3 | Kesari | In person, 9 October 2026, Dr. Ambedkar International Centre, New Delhi | Teams work under supervision, present, and defend assessments |

### Strategic Battle Windows for Round 1

1. **Portal Onboarding & Pre-Fight Readiness (14:00 - 17:00 | 3 Hours)**:
   - Portal access opens at 14:00. This is the platform where challenges and findings will be tracked.
   - Immediate tasks: Log in, verify credentials for all 3 members, inspect the tracking form fields, character limits, attachments, and scoring rubric.
   - Dry-run local environment: verify Docker daemon, tool availability (`semgrep`, `gitleaks`, `trivy`), and AI prompt setups.
   - *Goal*: Eliminate all logistical and platform friction before the repo drops at 17:00.
2. **Evaluation & Execution Window (17:00 - 23:00 | 6 Hours)**:
   - 17:00 - 17:45: Target repo released; clone immediately, spin up local container, launch automated scanners & AI prompt sweeps in parallel.
   - 17:45 - 18:30: Triage AI outputs, de-duplicate with scanner alerts, prune obvious False Positives.
   - 18:30 - 20:30: Dual Static (code data flow) and Dynamic (curl/runtime) verification of high-risk flaws.
   - 20:30 - 21:30: Attack chains, multi-step business logic, IDORs, and edge cases.
   - 21:30 - 22:30: Portal finding entry (Template A for TPs, Template B for FPs) and 3-member sign-off.
   - 22:30 - 23:00: Final freeze at 22:30, sanitize secrets, submit in portal by 22:45 (15-min safety buffer).

**VERIFY BEFORE COMPETITION:** scope statement, permitted endpoints, credentials, rate limits, write/destructive-test rules, required evidence format, AI/data handling rules, timebox, and submission deadline.

## 3. Team Structure

| Member | Primary ownership | Decision question |
| --- | --- | --- |
| 1 - Team Lead / Security Architect / Triage | Architecture, threat model, prioritisation, chains, final report, time, submission | What actually matters? |
| 2 - Application Security / Code Analysis | Source, SAST/SCA, secrets, authz/authn, business logic, delivery and infrastructure code | What does the code actually allow? |
| 3 - Dynamic / Adversarial / Defense Engineer | Safe runtime verification, request analysis, PoC evidence; contingency monitoring and IR | Can we safely make it happen? |

No critical finding is submitted as confirmed without, when time permits, all three lenses: impact (Member 1), source/data flow (Member 2), and reproduction/evidence (Member 3).

### Finding verdicts

| Verdict | Standard |
| --- | --- |
| CONFIRMED | Impact, source, and safe reproduction align |
| PARTIALLY CONFIRMED | Defect is real but claimed impact or reachability is unproven |
| LIKELY | Strong evidence, pending a stated dependency |
| UNRESOLVED | Material question remains; record the blocker |
| FALSE POSITIVE | No viable source-to-sink path, trust boundary, or exploit condition |
| DUPLICATE | Same root cause and impact as a canonical finding |
| OUT OF SCOPE | Credible issue outside authorised target or rules |

## 4. Team Communication

Use one shared findings board and one timestamped notes file. One message, one state:

~~~
[NEW] SEC-001 title, owner, component
[VERIFY] SEC-001 exact question / dependency
[CONFIRMED] SEC-001 evidence path, impact
[FALSE] SEC-001 reason and source-to-sink conclusion
[BLOCKED] SEC-001 missing access/log/rule
[CHAIN] CHAIN-01 SEC-001 -> SEC-004
[CRITICAL] SEC-001 immediate review needed
~~~

Interrupt immediately for a credible critical chain, a time-sensitive submission issue, evidence that invalidates a shared assumption, or a scope/safety concern. Otherwise batch updates every 10-15 minutes. Member 1 owns the canonical status and stops duplicate effort.

## 5. Tool Arsenal

Activate the supplied environment before the required scanners:

~~~
source ~/.security-tools/venv/bin/activate
which semgrep codeql osv-scanner gitleaks trivy
~~~

| Tool | Use now | It finds | Do not blindly trust |
| --- | --- | --- | --- |
| Semgrep | Early source triage | Pattern-level insecure code | Reachability, sanitisation, framework context |
| CodeQL | Early / parallel | Data flow and semantic patterns | Build coverage, source/sink model, exploitability |
| Gitleaks | Early | Secret-like strings and history | Whether value is active, exposed, or privileged |
| OSV-Scanner | Early | Known vulnerable dependencies | Actual use, reachable vulnerable path, fixed version context |
| Trivy | Early | Filesystem, dependency, IaC, image issues | Deployment exposure and compensating controls |
| Syft / Grype | When dependencies matter | SBOM / advisory correlation | Lockfile completeness and reachability |
| Burp Suite / ZAP | Only if runtime scope allows | Request/response differences, surface mapping | Automated attack claims and destructive tests |
| curl / jq / httpie | Runtime validation | Reproducible HTTP evidence | Authentication and object-ownership assumptions |
| git / ripgrep | Always | History, config, secret and call-site discovery | Generated/vendor files as application logic |
| nmap / Wireshark / mitmproxy | RULE-DEPENDENT | Authorised network observation | Scope, rate limits, benign competition traffic |
| Python / Docker tooling | As needed | Local execution, parsing, container inspection | That local setup equals organiser deployment |

Language branches: Python: pip-audit, Bandit; JavaScript/TypeScript: npm audit, OSV; Go: govulncheck; Rust: cargo audit; Java: CodeQL plus dependency tooling; PHP: Composer audit. Run only what matches the target.

For every tool record command, timestamp, target/commit, version, output path, coverage limitation, and verdict. See [COMMAND_CHEAT_SHEET.md](COMMAND_CHEAT_SHEET.md) for compact commands and failure modes.

## 6. Environment Setup

1. Confirm target directory, repository remote, branch, commit, language, framework, data stores, deployment files, APIs, auth model, and supplied logs.
2. Create a new evidence directory per target. Never mix targets or rounds.
3. Record source integrity before and after review:

~~~
git status --short
git rev-parse HEAD
git diff --stat
~~~

4. Keep assessment work read-only unless the organiser authorises modification. Preserve any authorised change separately with a before/after baseline.
5. Store raw scanner output; put conclusions in findings, not renamed scanner output.

## 7. Universal Assessment Methodology

~~~
Intake -> Architecture -> Automation -> Source trace -> Safe validation -> Impact -> Chain -> Report -> Cross-review -> Submit
~~~

For each candidate, trace: attacker-controlled input -> parser/transform -> authorisation decision -> sensitive sink -> affected asset. Then answer: who can reach it, what prerequisite is required, what changes or data exposure result, and what stops the claimed exploit.

Rejecting a false positive protects credibility, frees review time, and demonstrates exactly the judgment the announced format measures.

## 8. Round 1 - Vulnerability Assessment Architecture

### 8.0 Portal Onboarding & Pre-Fight Readiness (14:00 - 17:00)

*Portal access opens at 14:00 to track challenges, findings, and rules. The target Git repository is released at 17:00.*

1. **Portal Intake & Tracking Inspection (14:00 - 14:45 | M1)**:
   - Log into the official portal; confirm account access for all 3 members.
   - Inspect the finding submission mechanism: Required metadata fields, severity classification, True/False Positive flags, formatting guidelines (Markdown/PDF), and attachment size limits.
   - Record scoring rules, evaluation criteria, and any negative marking for invalid submissions.
2. **Tooling Pipeline Dry-Run & Test Setup (14:45 - 16:15 | M2 & M3)**:
   - Verify scanner environment (`semgrep`, `gitleaks`, `trivy`, `osv-scanner`, `codeql`).
   - Confirm Docker daemon is running and healthy.
   - Test LLM API keys and load [AI_PROMPTING_PLAYBOOK.md](AI_PROMPTING_PLAYBOOK.md) into AI workspaces.
   - Initialize clean directory structure (`scans/`, `evidence/`, `findings/`, `ai_outputs/`, `reports/`).
3. **Pre-Battle Alignment & Repo Drop Readiness (16:15 - 17:00 | All)**:
   - Review M1/M2/M3 role assignments and portal submission protocols.
   - At 17:00 sharp: Ingest repo, spin up Docker target, fire automated scanners, and execute AI prompt extraction.

### 8.1 AI-Assisted Vulnerability Discovery Pipeline

AI is explicitly permitted and required for candidate generation, but AI output is strictly treated as an **unverified hypothesis**:
1. **Extraction**: Use AI Prompt 1 & 2 to map routes and trace potential source-to-sink data paths.
2. **Adversarial Debunking**: Run the "Devil's Advocate" Prompt (Prompt 3) on every suspected finding to identify if framework auto-escaping, ORM parameterization, or upstream middleware invalidates the claim.
3. **Candidate Queue**: Promising leads move to the human verification queue; obvious hallucinations are documented for False Positive reporting.

### 8.2 Dual-Track Verification: Static Code + Dynamic Runtime

Every confirmed candidate must be proven through two distinct lenses:
- **Static Analysis (M2)**: Trace attacker-controlled input $\to$ validation/transform $\to$ authorization check $\to$ sensitive sink. Document file path and exact line numbers.
- **Dynamic Analysis (M3)**: Execute safe, non-destructive HTTP requests against the local target. Document curl command, HTTP status code, response body, and container log entries showing execution at the sink.

### 8.3 True Positive (TP) vs False Positive (FP) Standard

In a 921-team competition with only 50 qualifiers, the ability to weed out false alarms is evaluated just as heavily as finding real bugs. Use [TRUE_VS_FALSE_POSITIVE_GUIDE.md](TRUE_VS_FALSE_POSITIVE_GUIDE.md):
- **TRUE POSITIVE**: Flaw is reachable in production code, untrusted input reaches an unmitigated sink, and dynamic execution proves security impact.
- **FALSE POSITIVE**: Scanner or AI flagged an issue, but code inspection proves the input is non-attacker controlled, code is dead/unrouted, ORM safely binds parameters, or framework auto-sanitizes output. Must be documented using Template B in [FINDING_REPORT_TEMPLATE.md](FINDING_REPORT_TEMPLATE.md).

### 8.4 Attack Chains & Deep Business Logic

What scanners and AI models routinely miss:
- **IDOR / Tenant Boundaries**: Object access without server-side owner validation.
- **State Machine Tampering**: Skipping checkout steps, replaying tokens, price manipulation.
- **Mass Assignment**: Modifying privileged attributes (`role`, `is_verified`) via unrestricted JSON body.
- **Exploit Chains**: Chaining an informational data leak with a medium authorization flaw to achieve critical account takeover.

### 8.5 Reporting & Peer-Review Gate (21:30 - 22:30)

No finding is submitted without passing the 3-Member Sign-off Gate:
- **M1**: Verifies demonstrated business impact, justified severity, and clean formatting.
- **M2**: Verifies code dataflow, accurate file/line references, and remediation code diff.
- **M3**: Verifies reproducible curl command, response logs, and safe execution.
- **Submission Buffer**: Content freeze at 22:30; submit by 22:45 to avoid portal overload.

## 9. Round 2 - Defense

**RULE-DEPENDENT:** the PIB notice calls this the online Dangal and does not state a defense/attack format. Use this section only where supplied rules create a monitored target.

### 9.1 Baseline

Before any attack window, capture expected processes, services, listeners, users, scheduled tasks, file hashes/locations, authentication activity, HTTP/API behaviour, outbound destinations, CPU, memory, and disk. Time-stamp every capture and document known competition tooling.

### 9.2 Monitoring

Member 2 owns host/application review: auth changes, errors, unusual routes, write operations, config modifications, and database anomalies. Member 3 owns network/detection/containment: connections, scans, request bursts, shells, unexpected outbound traffic, and persistence. Member 1 is Incident Commander and decides whether action risks availability.

### 9.3 Detection

Prioritise failed or impossible logins, new privileged accounts/tokens, endpoint enumeration, payload anomalies, high request rates, unexpected processes, scheduled-task/service edits, new listeners, reverse connections, lateral movement, mass reads, and destructive queries. Compare against baseline before declaring malicious activity.

### 9.4 Investigation

~~~
Detect -> Validate -> Scope -> Contain -> Eradicate -> Recover -> Verify -> Document
~~~

Preserve raw logs, process metadata, network facts, timestamps, affected accounts, and before/after state. Distinguish organiser traffic, teammate tests, and attack traffic using an agreed activity log.

### 9.5 Containment

Choose the narrowest reversible action first: revoke a suspect token, remove a new account, block a known hostile route, isolate a nonessential component, or restore known-good configuration. Confirm scope and authorisation before stopping shared services. Member 1 approves availability-impacting actions.

### 9.6 Recovery

Remove confirmed persistence or exposed credential, restore a known-good state, retest the original signal, monitor for recurrence, and document residual risk. A restart alone is not eradication.

### 9.7 Evidence

Preserve immutable copies where possible. Note source, collection method, timestamp/time zone, target, handler, checksum, and every transformation. Do not collect or disclose unrelated personal or credential data.

## 10. Round 3 - Offensive Assessment

**RULE-DEPENDENT:** Kesari is publicly described as a supervised, in-person assessment and defense. It is not publicly described as red teaming. Use active testing only to the extent the organiser scope explicitly permits.

### 10.1 Recon

Map repository structure, deployment topology, routes, identities, objects, roles, data classes, background jobs, webhooks, protocols, third-party dependencies, and trust boundaries.

### 10.2 Enumeration

Enumerate from supplied source/docs and authorised runtime behaviour. Record endpoint, method, role, object type, input, output, side effect, and data owner. Prefer source-derived routes over blind fuzzing.

### 10.3 Authentication

Look for credential reset/recovery flaws, inconsistent middleware, session fixation/expiry gaps, JWT validation/claim confusion, OAuth/OIDC redirect and binding mistakes, SSO trust boundaries, and internal endpoints reachable without the intended identity. Safe test: compare an unauthenticated, valid low-privilege, and expected privileged request.

### 10.4 Authorization

Use the matrix in [MASTER_VULNERABILITY_CHECKLIST.md](MASTER_VULNERABILITY_CHECKLIST.md). Check every object action server-side: list, read, create, update, delete, export, approve, admin action, and internal route. A client-hidden button proves nothing.

### 10.5 API

Inspect REST, GraphQL, WebSocket, webhook, and async interfaces for server-enforced identity, schema validation, mass assignment, pagination exposure, rate limits, replay resistance, signature verification, tenant context, and error leakage. Safe test: change one identity/object/field at a time and compare policy outcomes.

### 10.6 Business Logic

Draw state transitions, for example CREATED -> PENDING -> APPROVED -> PAID -> COMPLETED. Test authorised transitions versus skip, repeat, reverse, replay, ownership change, price/input modification, and concurrent requests. Evidence requires expected policy plus actual accepted transition.

### 10.7 Injection

Trace untrusted input into queries, interpreters, templates, file paths, deserializers, shell/process invocation, and downstream services. Confirm escaping/parameterisation in the exact active branch. Use harmless, scope-approved canaries; do not execute destructive payloads.

### 10.8 SSRF

Find server-side URL fetches, importers, renderers, webhook relays, previewers, and AI tools. Check URL parsing after redirects/DNS resolution, allowed destinations, metadata/internal ranges, response handling, and data disclosure. Validate only with organiser-provided harmless endpoints.

### 10.9 Files

Review upload/download path construction, canonicalisation, extension/content mismatch, storage visibility, size limits, archive handling, signed URLs, and post-processing. Safe proof is a policy-bypassing filename or controlled non-executable sample, never a malicious file.

### 10.10 Secrets

Trace each secret from repository/config/log to runtime permission and exposure. Differentiate example, dead, encrypted, revocable, and active credentials. Report capability, not merely appearance.

### 10.11 Infrastructure

Review Dockerfiles, compose/Kubernetes/IaC, CI/CD, images, registries, service accounts, IAM policies, ingress, network egress, databases, backups, and environment injection. Look for defaults, privilege, public reachability, plaintext secrets, mutable tags, and missing segmentation.

### 10.12 AI/LLM

Model User -> LLM -> Tool -> Database/API -> Sensitive action. Test whether untrusted direct or retrieved content can influence tool choice, arguments, identity, tenant, data scope, memory, or system instruction. Require server-side tool authorization independent of model output. For RAG, inspect source trust, retrieval partitioning, sensitive context exposure, citations, and ingestion controls. For MCP/tool calling, verify least privilege, explicit allowlists, schemas, confirmation for sensitive actions, and per-user authorization.

### 10.13 Attack Chains

Link only proven or clearly labelled conditional steps. A Medium issue becomes Critical only when the chain demonstrates practical reach to a high-value impact. Do not multiply severity merely because a hypothetical next step exists.

### 10.14 PoC

Keep a minimal, non-destructive proof that another assessor can repeat in scope. Include setup, exact safe input/request, observed output, source/log evidence, cleanup, and constraints. Never embed live credentials or unsafe payloads.

### 10.15 Reporting

Report root cause, impact, likelihood, affected assets, evidence, fix, and regression test. For a disputed claim, explain the rejected path as carefully as the accepted one.

## 11. Vulnerability Checklists

Use [MASTER_VULNERABILITY_CHECKLIST.md](MASTER_VULNERABILITY_CHECKLIST.md) as the canonical checklist. The priority order is: authorization, authentication/session, business logic, untrusted-input paths, files/SSRF/webhooks, secrets/dependencies, infrastructure, AI/tool boundaries.

## 12. False Positive Methodology

~~~
Finding -> Trace source -> Identify input -> Identify sink -> Trust boundary -> Exploitability -> Impact -> Verdict
~~~

Mark an alert false only with a positive reason: dead path; non-attacker-controlled input; enforced allowlist; safe parameterization; downstream permission denial; non-production artifact; duplicate root cause; or missing precondition. “Could not reproduce” alone is UNRESOLVED unless the code/path establishes safety.

## 13. Severity Methodology

Severity is a judgment of **exploitability x impact x exposure x business criticality**.

| Severity | Meaning |
| --- | --- |
| Critical | Practical path to severe cross-tenant/system compromise, sensitive-data exposure, or irreversible high-impact action |
| High | Credible significant impact with realistic prerequisites |
| Medium | Real defect with bounded impact, privileged/preconditioned reach, or missing chain |
| Low | Limited impact, hard-to-reach weakness, or defence-in-depth gap |
| Informational | Useful observation without a demonstrated security impact |

Downgrade a scanner Critical when the vulnerable feature is unreachable, non-production, blocked by a verified control, or lacks meaningful impact. Upgrade a Medium only when an evidenced chain removes its constraints.

## 14. Evidence Management

~~~
competition/
├── target/
├── baseline/
├── scans/
├── evidence/
├── findings/
├── poc/
├── screenshots/
├── reports/
└── notes/
~~~

Every evidence item records timestamp and zone, target, commit, collector, command/request, raw result, redaction, and relation to finding ID. Maintain a README.md in each round directory with scope and source-integrity record.

## 15. Command Cheat Sheet

Use [COMMAND_CHEAT_SHEET.md](COMMAND_CHEAT_SHEET.md). Commands are intentionally compact and must be constrained by organiser authorisation.

## 16. Decision Trees

### Authentication issue

~~~
Unauthenticated reachability?
  -> Sensitive function or data?
    -> Another user's object?
      -> Privileged operation?
        -> Evidence, impact, severity
~~~

### Reported SQL injection

~~~
Attacker-controlled input? -> Dynamic query? -> Parameterized at actual sink?
  -> Escapes syntax? -> Read or write impact? -> Confirm / reject / unresolved
~~~

### Secret found

~~~
Real value? -> Active or historical? -> Accessible to attacker? -> Permissions?
  -> Reachable asset / impact -> Severity and redacted evidence
~~~

## 17. Time-Boxed Strategies

### Confirmed Round 1 Master Schedule (15 September 2026)

| Phase | Time Window | Team Focus | Deliverables |
| --- | --- | --- | --- |
| **Phase 0: Portal Recon** | **14:00 - 17:00 (3h)** | Log into competition tracking portal, inspect submission schema/limits, dry-run scanners, and test AI prompt setups | Portal access confirmed, environment verified, tool pipelines ready |
| **Phase 1: Repo Ingest & Scans** | **17:00 - 17:45 (45m)** | Target repo released! Clone repo, spin up Docker container, launch automated scanners (Semgrep, CodeQL, Gitleaks, Trivy), and run batch AI prompts | Running local container, raw scan JSONs, initial AI candidate queue |
| **Phase 2: Triage** | **17:45 - 18:30 (45m)** | Merge AI findings + tool alerts into canonical `SEC-XXX` IDs; weed out dead code and obvious AI hallucinations | Assigned high-value candidate queue |
| **Phase 3: Deep Proof** | **18:30 - 20:30 (2h)** | Dual verification: M2 traces code source-to-sink; M3 executes safe curl requests against running app | Confirmed True Positives with static line numbers + dynamic HTTP proof |
| **Phase 4: Chains & Logic** | **20:30 - 21:30 (1h)** | Audit business logic, IDOR/BOLA, privilege escalation, and multi-step attack chains | High/Critical chain findings, edge-case vulnerability proofs |
| **Phase 5: Portal Entry & Report** | **21:30 - 22:30 (1h)** | Enter findings into portal tracking system (Template A & B); conduct 3-Member Peer Review | Completed portal entries and verified finding reports |
| **Phase 6: Submission Freeze** | **22:30 - 23:00 (30m)** | **22:30 Content Freeze**; submit via portal by 22:45, verify receipt and store checksummed backup | Portal confirmation receipt and archive hash |

Member 1 sets timeboxes. End a hypothesis when a required precondition is unsupported, the branch is dead, the evidence cannot change final ranking, or its time budget expires; record why and move on.

## 18. Three-Member Role Cards

See [RESPONSIBILITY_MATRIX.md](RESPONSIBILITY_MATRIX.md). Member 1: architecture, triage, impact, integration, submission. Member 2: scans, source/data flow, authz/business/infrastructure review. Member 3: safe runtime proof, requests, evidence, and the rule-dependent defense workflow.

## 19. Training Plan

Use [TRAINING_ROADMAP.md](TRAINING_ROADMAP.md). Practice only legal labs and local deliberately vulnerable applications. Train the handoff: discovery -> source proof -> safe reproduction -> concise report.

## 20. Competition-Day Checklist

Open [COMPETITION_DAY_CHECKLIST.md](COMPETITION_DAY_CHECKLIST.md) at the start of every round. The first ten minutes are scope, integrity, evidence structure, architecture, and role allocation.

## 21. Final Submission Checklist

- Scope and target/commit are correct.
- Every confirmed finding has source/data-flow evidence and safe proof or an explicit reason it lacks runtime proof.
- Severity matches demonstrated impact, not scanner labels.
- Duplicates link to one canonical root cause.
- False positives state why they are false.
- Secrets and sensitive evidence are redacted.
- Attack-chain links are proven or labelled conditional.
- Fixes are concrete and include regression checks.
- Report language distinguishes fact, inference, and unknown.
- Submission format, filenames, and deadline were verified from organiser instructions.

## 22. Lessons-Learned Template

~~~
Round / target / date:
What did we correctly confirm?
What did we correctly reject?
What did we miss or mis-prioritise?
Which assumption was wrong?
Which handoff delayed us?
Which command/template saved time?
Which evidence was insufficient?
One checklist change before the next round:
One practice scenario before the next round:
Owner and due date:
~~~

## Quick Operating Rule

When unsure what to do next: identify the highest-impact unverified candidate, assign the missing lens (impact, source, or proof), set a short timebox, record the verdict, and move on.

