# CYBER KUSHTI 2026 - TRUE POSITIVE VS FALSE POSITIVE TRIAGE GUIDE

> **THE 921 $\to$ 50 FILTER**: In a pool of 921 teams, automated scanner dumps and raw AI hallucinations will be eliminated in the first round of judging. Distinguishing real security defects from false alarms—and defending that determination with code-grounded proof—is what puts a team in the top 5.4%.

---

## 1. The Evidentiary Standards

| Attribute | True Positive (TP) Standard | False Positive (FP) Standard |
| --- | --- | --- |
| **Static Evidence** | Verified source-to-sink data flow in production code. No effective sanitization or authorization check. | Demonstrates where the flow breaks: auto-escaping, schema validation, dead code, or upstream middleware guard. |
| **Dynamic Evidence** | Working, non-destructive curl/HTTP request showing unauthorized state change, data leak, or sink execution. | Dynamic request returns expected rejection (e.g. 400 Bad Request, 403 Forbidden) or proves harmless handling. |
| **Impact** | Practical business/technical consequence (data exposure, privilege escalation, bypass). | Theoretical or zero impact; input cannot manipulate sensitive assets. |
| **Judge Impression** | "This team proved a genuine security flaw down to the code and runtime." | "This team has real security expertise; they didn't fall for automated scanner noise." |

---

## 2. Top 10 False Positive Archetypes in Code Auditing

When reviewing alerts from AI, Semgrep, CodeQL, or SCA scanners, systematically test against these 10 patterns:

### 1. Dead Code / Unrouted Functions
- **Scanner/AI Claim**: "Dangerous `exec()` or raw SQL query found in `src/utils/legacy_export.py`."
- **How to Debunk (FP)**:
  1. Run `rg "legacy_export" src/` across the repository.
  2. Prove that the function is never imported, never invoked in any route, and is completely unreachable from external HTTP/API traffic.
- **Verdict**: **FALSE POSITIVE** (Unreachable / Dead Code).

### 2. Framework Auto-Sanitization / Auto-Escaping
- **Scanner/AI Claim**: "Cross-Site Scripting (XSS) in user profile render template."
- **How to Debunk (FP)**:
  1. Check template engine settings (e.g. Jinja2 `autoescape=True`, React JSX default escaping, Blade `{{ $var }}`).
  2. Unless explicit raw tags are used (e.g. `| safe`, `dangerouslySetInnerHTML`), the framework HTML-encodes output by default.
- **Verdict**: **FALSE POSITIVE** (Framework Auto-Sanitization).

### 3. ORM Parameterization Masked as String Interpolation
- **Scanner/AI Claim**: "SQL Injection in database query: `query = f'SELECT * FROM users WHERE id = :id'`."
- **How to Debunk (FP)**:
  1. Inspect the database execution call. If the ORM (SQLAlchemy, Prisma, Hibernate) uses named parameter binding (`:id`, params={'id': val}), the database driver executes a prepared statement regardless of Python f-string or string format wrapper.
- **Verdict**: **FALSE POSITIVE** (Prepared Statement / Parameterized Binding).

### 4. Controller-Level Upstream Middleware Guards
- **Scanner/AI Claim**: "Missing authorization check inside `deleteUser()` handler."
- **How to Debunk (FP)**:
  1. Look above the individual handler function.
  2. If the router or class declaration has `@UseGuards(AdminAuthGuard)` or `router.use(verifyAdmin)`, all child handlers inherit strict authorization before code execution.
- **Verdict**: **FALSE POSITIVE** (Inherited Upstream Middleware Protection).

### 5. Schema Validation / Strict DTO Type Enforcement
- **Scanner/AI Claim**: "Mass assignment vulnerability allows modifying user status to admin."
- **How to Debunk (FP)**:
  1. Inspect the input parser (e.g. Pydantic model, Zod schema, Joi, or strict DTO with `whitelist: true`).
  2. If the schema explicitly defines allowed fields (`username`, `email`) and strips or throws errors on undeclared fields (`is_admin`), mass assignment is impossible.
- **Verdict**: **FALSE POSITIVE** (Schema Whitelisting / DTO Enforcement).

### 6. Non-Attacker-Controlled Sinks
- **Scanner/AI Claim**: "Command Injection in `subprocess.Popen(command)`."
- **How to Debunk (FP)**:
  1. Trace `command` backwards to its origin.
  2. If `command` is derived purely from an internal configuration file, an environment variable set by DevOps, or a hardcoded dictionary, an external attacker cannot inject commands.
- **Verdict**: **FALSE POSITIVE** (Input Not Controllable by Attacker).

### 7. Test Fixtures, Mocks & Seed Files
- **Scanner/AI Claim**: "Hardcoded high-entropy secret / API token found."
- **How to Debunk (FP)**:
  1. Inspect the file path: `tests/fixtures/mock_keys.json`, `seeds/seed_users.js`, or `.env.example`.
  2. Confirm this is dummy test data, not packaged in the production Docker container or accessible in production environments.
- **Verdict**: **FALSE POSITIVE** (Test Fixture / Non-Production Secret).

### 8. Dev-Only / Build-Time Dependency Alerts (SCA Noise)
- **Scanner/AI Claim**: "Critical CVE-XXXX in package `webpack-dev-server` or `nodemon`."
- **How to Debunk (FP)**:
  1. Inspect `package.json` under `devDependencies`.
  2. Verify that in the production `Dockerfile`, dependencies are installed via `npm ci --production` or `pip install --no-dev`.
  3. The vulnerable package never runs in the production target.
- **Verdict**: **FALSE POSITIVE** (Development Dependency / Non-Shipped).

### 9. Early Return / Preceding Validation Guards
- **Scanner/AI Claim**: "Path Traversal in file downloader: `open(BASE_PATH + user_filename)`."
- **How to Debunk (FP)**:
  1. Check lines immediately preceding the sink: `if ".." in user_filename or "/" in user_filename: raise BadRequest()`.
  2. The input is strictly sanitized or rejected before reaching the filesystem sink.
- **Verdict**: **FALSE POSITIVE** (Preceding Validation Guard).

### 10. Safe Parsers Flagged as Insecure Deserialization
- **Scanner/AI Claim**: "Insecure Deserialization in YAML/JSON loader."
- **How to Debunk (FP)**:
  1. Inspect the method call: `yaml.safe_load()` instead of `yaml.load()`, or native `JSON.parse()`.
  2. `yaml.safe_load()` restricts deserialization to simple data types and does not execute arbitrary code.
- **Verdict**: **FALSE POSITIVE** (Safe Deserializer Implementation).

---

## 3. The 3-Step Human Verification Routine

Whenever an AI model or automated tool outputs a vulnerability alert, follow this 3-step verification process:

```text
[Alert: "Vulnerability in file X, line Y"]
                   │
                   ▼
Step 1: Code Reality Check (M2)
- Open the actual repo at line Y. Does this code exist?
- Does the parameter originate from user input?
- Is there any sanitizer, middleware, or early return?
                   │
         ┌─────────┴─────────┐
      Safe/Dead           Vulnerable
         │                   │
         ▼                   ▼
   [Mark FALSE         Step 2: Dynamic Execution Check (M3)
    POSITIVE]          - Send test request to localhost.
                       - Does application accept the payload?
                       - What does the response/log prove?
                             │
                   ┌─────────┴─────────┐
                Blocked              Triggered
                   │                   │
                   ▼                   ▼
             [Mark FALSE         Step 3: Impact & Chain (M1)
              POSITIVE]          - What is the real consequence?
                                 - Can this chain with other bugs?
                                 - Mark TRUE POSITIVE.
```

---

## 4. Writing an Award-Winning False Positive Rejection

When submitting False Positive findings to the judges, follow this concise, professional format (Template B in [FINDING_REPORT_TEMPLATE.md](FINDING_REPORT_TEMPLATE.md)):

```markdown
### FP-004: Debunking Claimed SQL Injection in Search API
- **Original Alert**: Semgrep rule `python.django.security.raw-sql` flagged `views.py:44`.
- **Claim**: Attacker can inject arbitrary SQL queries via `?query=` parameter.
- **Technical Reality (False Positive)**:
  1. While the function uses raw SQL, the input is passed as a parameterized tuple: `cursor.execute("SELECT * FROM items WHERE name = %s", [query])`.
  2. The Django DB adapter automatically handles escaping and parameterization at the database driver level.
  3. Dynamic testing with canary `' OR '1'='1` was safely treated as a literal search string returning 0 results, confirming no syntax escape occurs.
- **Verdict**: **FALSE POSITIVE** (Safe Parameterization Verified).
```
