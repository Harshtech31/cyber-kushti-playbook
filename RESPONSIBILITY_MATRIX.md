# CYBER KUSHTI 2026 - THREE-MEMBER RESPONSIBILITY MATRIX

| Activity | M1: Lead / Architect / Triage | M2: AppSec / Code | M3: Dynamic / Runtime |
| --- | --- | --- | --- |
| Scope, clock, portal setup (14:00) | **Own** | verify | verify |
| Portal tracking & schema inspection | **Own** | support | support |
| Repo clone & fingerprinting (17:00) | **Own** | verify | verify |
| Local Docker/runtime build (17:10) | review | support | **Own** |
| Scanners (Semgrep/CodeQL/Trivy/Gitleaks) | triage | **Own** | review coverage |
| AI Prompting & Code Sweeps | **Own (Prompts 1 & 3)** | **Own (Prompt 2)** | **Own (Prompt 4)** |
| Static source-to-sink trace | challenge impact | **Own** | correlate runtime |
| Dynamic curl / runtime verification | define impact | inspect handlers | **Own** |
| True Positive (TP) full validation | approve business impact | **Own static proof** | **Own runtime proof** |
| False Positive (FP) technical debunk | verify rejection logic | **Own code proof** | **Own runtime check** |
| Attack chains & business logic | **Own** | validate technical path | validate feasibility |
| Portal findings entry & reporting | **Own (Template A & B)** | technical code review | reproduction review |
| Final 22:45 portal submission dispatch | **Own** | verify package | verify upload receipt |

## Role Cards

### Member 1 - Team Lead / Security Architect / Triage

**Do immediately:** scope, commit, deadline, assets/roles/data map, shared board, top risks.

**Monitor:** coverage gaps, duplicate effort, unproven high-severity claims, time remaining, submission requirements.

**Decide:** severity, candidate timeboxes, chain priority, scope escalation, availability-impacting containment, final wording.

**Do not waste time on:** re-running every scanner, lengthy PoCs for already-bounded Low issues, or becoming the only note-taker.

### Member 2 - Application Security / Code Analysis

**Exact workflow:** map entry points -> run target-specific scans -> group alerts -> trace input to sink -> inspect authz before data access -> inspect state changes/config/dependencies -> post evidence and verdict.

**Manual priorities:** ownership/tenant checks, auth/session/JWT/OAuth, mass assignment, business state, validation/sinks, webhooks/SSRF, files, crypto/secrets, Docker/CI/IaC, AI tool boundaries.

**Do not claim:** a scanner result without path/conditions, a dependency advisory without relevance, or a secret without capability/exposure analysis.

### Member 3 - Dynamic / Adversarial / Defense

**Exact workflow:** map authorised routes -> establish expected behavior -> vary one identity/object/input at a time -> preserve request/response -> correlate source/log -> write safe repeatable proof.

**Burp/ZAP:** use for authorised request capture, controlled comparison, and surface mapping; do not launch unbounded or destructive automation.

**Round 2:** collect baseline, validate alerts, scope, execute approved narrow containment, preserve logs/process/network facts, verify recovery.

## Critical Finding Gate

| Lens | Owner | Required question |
| --- | --- | --- |
| Impact | M1 | What affected asset and business/security consequence are real? |
| Source | M2 | Does the actual branch and data flow support the claim? |
| Proof | M3 | Can it be safely reproduced in scope? |

If one lens is missing, downgrade confidence or state the dependency. Do not invent certainty.

