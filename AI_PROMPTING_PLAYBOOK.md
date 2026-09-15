# CYBER KUSHTI 2026 - AI PROMPTING PLAYBOOK FOR CODE AUDITING

> **OBJECTIVE**: Systematically leverage AI (Claude, GPT, Gemini, or local models) to uncover hidden vulnerabilities across a target repository, generate candidate hypotheses, aggressively test for False Positives, and synthesize harmless dynamic reproduction steps.

---

## 1. Operating Rules for AI in Cyber Kushti

1. **AI is a Hypothesis Generator, Not a Judge**: AI models hallucinate vulnerabilities when looking at code without seeing surrounding framework contexts. Never trust an AI finding without verifying the exact file and lines in the repository.
2. **Chunk Strategically**: Do not dump 50 files into one prompt. Audit the application in logical slices:
   - Slice 1: Authentication, Session & Role Middleware.
   - Slice 2: Routes & Controllers (Entry points).
   - Slice 3: Business Logic & State Machines (Orders, Payments, Approvals).
   - Slice 4: Data Layer, File Handling, and External Integrations (SSRF, Webhooks).
3. **Always Run the "Devil's Advocate" Prompt**: Before committing time to test an AI-suggested vulnerability dynamically, ask the AI to argue why the finding might be a **False Positive**.

---

## 2. Prompt 1: Architecture & Attack Surface Extractor

*Use upon repo release (17:00) during Phase 1 to map out what the target repository actually does.*

```text
You are a Principal Security Architect auditing a target codebase for an elite vulnerability assessment competition.

Analyze the provided repository files (directory tree, dependency manifests, and route definitions):
[PASTE DIRECTORY TREE, PACKAGE MANIFEST, DOCKERFILE, AND MAIN ROUTER FILE]

Deliver a concise threat modeling breakdown containing:
1. Technology Stack: Languages, web framework, database, ORM, authentication libraries.
2. Trust Boundaries: Where do external/untrusted users interact with internal services?
3. Identity & Roles: What roles exist (e.g. Anonymous, Registered User, Admin, Service Account)?
4. Sensitive Operations: List top 5-10 high-value endpoints (e.g. money transfer, password change, file upload, internal admin).
5. High-Risk Attack Surface: Identify which files/controllers appear most prone to IDOR, injection, auth bypass, or SSRF based on dependencies and routing.
```

---

## 3. Prompt 2: Deep Vulnerability Hunter (Source-to-Sink)

*Use to audit specific controllers, route handlers, and service files.*

```text
You are an expert Application Security Assessor. Audit the following source code for real, exploitable security vulnerabilities.

Target Code:
```[LANGUAGE]
[PASTE CODE FILE OR RELEVANT CONTROLLER & SERVICE]
```

Audit Focus:
1. Authorization & Tenant Isolation (IDOR, BOLA, missing role checks, horizontal/vertical privilege escalation).
2. Authentication & Session Flaws (token verification, parameter pollution, account takeover).
3. Business Logic & State Tampering (price tampering, step skipping, replay attacks, race conditions).
4. Injection Flaws (SQL, NoSQL, Command, Template, LDAP injection).
5. Server-Side Request Forgery (SSRF) & Insecure File Processing (path traversal, arbitrary upload).
6. Mass Assignment / Object Injection (unfiltered client JSON modifying internal fields).

Output Requirements:
For each vulnerability found, strictly output in this format:
- Finding Title:
- Severity (Critical/High/Medium/Low) with justification:
- Attacker Input Vector: [Exact parameter, header, or body field]
- Source-to-Sink Path:
  - Source: [File and line where input enters]
  - Sink: [File and line where dangerous operation executes without check]
- Root Cause: [Why the vulnerability exists]
- Exploit Scenario: [How an attacker triggers this in practice]
- False Positive Risk: [What might prevent this from working in a real runtime?]
```

---

## 4. Prompt 3: The Adversarial Devil's Advocate (False Positive Sifter)

*CRUCIAL FOR THE 921-TEAM FILTER: Run this on every candidate finding before spending time on dynamic testing.*

```text
You are a ruthless Senior Security Auditor whose job is to disprove vulnerabilities and catch False Positives. 

Review this suspected vulnerability candidate against the provided source code:

Suspected Finding:
[PASTE FINDING SUMMARY, SUSPECTED SOURCE, AND SINK]

Full Context / Surrounding Code:
```[LANGUAGE]
[PASTE RELEVANT CODE, MIDDLEWARE, AND CONFIGURATION]
```

Critically evaluate whether this is a TRUE POSITIVE or a FALSE POSITIVE:
1. Does the framework or ORM automatically sanitize, parameterize, or escape this input?
2. Is there upstream middleware (e.g. auth check, schema validation, rate limiter) that blocks this request?
3. Is this route or function actually exposed and reachable from outside, or is it dead/internal/test code?
4. Is the parameter truly controlled by an external attacker, or is it a hardcoded or server-side value?

Verdict:
Conclude with either:
- "CONFIRMED TRUE POSITIVE": State the exact conditions required for exploitation.
- "PROBABLE FALSE POSITIVE": State the exact code or framework protection that renders this unexploitable.
```

---

## 5. Prompt 4: Dynamic PoC & Verification Request Generator

*Use to generate safe, non-destructive curl commands and verification steps for M3.*

```text
You are a penetration tester preparing safe, non-destructive reproduction steps for a confirmed code vulnerability.

Vulnerability Details:
- Target Endpoint: [e.g. POST /api/v1/users/{id}/update]
- Vulnerability: [e.g. Mass Assignment allowing privilege escalation to admin]
- Vulnerable Code:
```[LANGUAGE]
[PASTE RELEVANT CONTROLLER SNIPPET]
```

Generate:
1. A safe, non-destructive curl command to reproduce and verify this issue against `http://localhost:8080`.
   - Use safe canary values (e.g. test parameters, benign probes); do NOT use destructive or DoS payloads.
   - Include all necessary headers (Content-Type, Bearer auth tokens if needed).
2. Expected Safe Behavior (What an authorized/secure system should return, e.g. HTTP 403 or filtered response).
3. Vulnerable Behavior (What the vulnerable application returns, e.g. HTTP 200 with modified field).
4. Container / Application Log Marker (What log entry or console output will prove execution reached the vulnerable sink).
```

---

## 6. Prompt 5: Remediation Patch & Regression Test Generator

*Use during Phase 5 (21:30 - 22:30) to generate the fix diff and regression test for the report and portal entry.*

```text
You are a Senior Software Security Engineer. Provide a robust, production-grade root cause fix for this vulnerability.

Vulnerable Code:
```[LANGUAGE]
[PASTE VULNERABLE CODE BLOCK]
```

Issue: [BRIEF SUMMARY OF DEFECT]

Deliver:
1. Unified Git Diff: A minimal, precise `diff` that fixes the vulnerability at the root cause without breaking application functionality.
2. Code Explanation: 2 sentences explaining why this fix completely eliminates the vulnerability.
3. Regression Test: A small unit or integration test (in pytest, jest, or standard curl test script) that:
   - Fails on the unpatched code.
   - Passes on the patched code.
```

---

## 7. Repo Auditing Chunking Protocol (Token Budget Management)

When auditing a multi-thousand line repository under time pressure:

| Priority | Directory / Component | What to Look For | AI Model Strategy |
| --- | --- | --- | --- |
| **Tier 1 (High Impact)** | `middleware/`, `auth/`, `routes/`, `controllers/` | Auth bypass, IDOR, routing flaws, unauthenticated endpoints | High-context window model (Prompt 2) |
| **Tier 2 (High Impact)** | `services/`, `handlers/`, `api/` | Business logic, state manipulation, SSRF, injection sinks | Chunk file-by-file with service context |
| **Tier 3 (Medium Impact)** | `models/`, `db/`, `migrations/` | Insecure queries, mass assignment fields, raw SQL | Run Semgrep first, feed alert context to AI |
| **Tier 4 (Low Impact)** | `config/`, `docker-compose.yml`, `.env.example` | Default credentials, insecure flags, exposed debug ports | Scan with Gitleaks + Trivy first |
| **Ignore / Low Priority** | `tests/`, `docs/`, `vendor/`, `node_modules/` | False positive traps! Do not spend prompt tokens here | Filter out via `.gitignore` / `rg` |
