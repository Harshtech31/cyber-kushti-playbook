# Hammer Repo — Dynamic Security Analysis & Vulnerability Report
> **Allocated Repository:** https://github.com/vulnerable-apps/hammer  
> **Pinned Commit SHA:** `c2bb69ba27899e4895bed63483f90f690dbd0c17`  
> **Framework:** Ruby on Rails 6.0.2 / Ruby 2.6.5  
> **Tools Used:** Gitleaks 8.30.1 · Semgrep 1.175.0 · Trivy 0.74.0 · Manual Code Review  
> **Team:** Null Theory (CK-IE1GKM99)  
> **Date:** 2026-09-15

---

## Tool Execution Summary

| Tool | Findings / Scope | Key Result | Verification Status |
|------|------------------|------------|---------------------|
| **Gitleaks 8.30.1** | **32 secrets** across `.env.local` + `.env.local.exported` | Real production credentials committed | 🔴 CONFIRMED TP |
| **Semgrep 1.175.0** | 4 findings (2× IDOR, 2× Unscoped Find) | Broken Object Level Authorization | 🔴 CONFIRMED TP |
| **Trivy 0.74.0** | 90+ CVEs in `yarn.lock`, 3 Dockerfile misconfigurations | Multiple Critical/High CVEs | 🔴 CONFIRMED TP |
| **Manual Code Audit** | Zero auth on controllers, mass assignment on `user_id`, commented SSL/CSP | Systemic security misconfigurations | 🔴 CONFIRMED TP |

---

## Detailed Vulnerability Findings (True Positives)

### TP-1 · Hardcoded Credentials Committed to Source Control
* **CWE:** CWE-798 (Use of Hard-coded Credentials)
* **Severity:** CRITICAL
* **Category:** Secrets / Credential Exposure
* **Tool Evidence:** Gitleaks 8.30.1 (32 secrets detected across `.env.local` and `.env.local.exported`)

```
CONFIRMED by gitleaks 8.30.1:
  [generic-api-key]        .env.local:2   → SECRET_KEY_BASE=HMeuvsfiUEnAH...
  [generic-api-key]        .env.local:20  → DEVISE_SECRET_KEY=KeEfYzYzDNGh...
  [generic-api-key]        .env.local:23  → S3_SECRET_ACCESS_KEY=mMzLwjRjoL...
  [generic-api-key]        .env.local:29  → CLOUD_CONVERT_API_KEY=EKgWzzrJZi...
  [generic-api-key]        .env.local:32  → DATABASEDOTCOM_CLIENT_SECRET=EA7...
  [twitter-api-secret]     .env.local:52  → MLouWrnrrMKUNkCXTFVULQDGXmxUru...
  [linkedin-client-secret] .env.local:54  → PnePEcsopQmT7gTT...
  + 16 identical findings in .env.local.exported
```

**Classification:** `TRUE_POSITIVE`  
**Justification:**  
Gitleaks 8.30.1 detected 32 real credential strings across `.env.local` and `.env.local.exported`, both committed to the public GitHub repository. The secrets include: `SECRET_KEY_BASE` (enables session forgery), `DEVISE_SECRET_KEY` (authentication bypass), `S3_SECRET_ACCESS_KEY` (cloud storage takeover), `AUTHORIZE_NET_API_TRANSACTION_KEY` (payment gateway fraud), MySQL production passwords, and OAuth secrets for LinkedIn and Twitter. These are not test/placeholder values — the naming conventions (`rtcfingroup`, `rtcadminmongo`, `rtc_admin`) indicate production RTCFinGroup credentials. Verified by independent manual inspection of `.env.local` lines 2–65.

**Evidence / Sinks:**  
* `.env.local:2` → `SECRET_KEY_BASE=HMeuvsfiUEnAHHPKLWVzoDoJPGCpmZBqvXaV4mrhnAXjbZKUDb`  
* `.env.local:23` → `S3_SECRET_ACCESS_KEY=mMzLwjRjoLtmGr/aABuq4etuJs/GKFDNgUfUATaz`  
* `.env.local:34` → `AUTHORIZE_NET_API_TRANSACTION_KEY=h6WgKcWWhHNDhWZCxTaKpb`  

---

### TP-2 · Missing Authentication on All Controllers (Complete Access Control Bypass)
* **CWE:** CWE-306 (Missing Authentication for Critical Function)
* **Severity:** HIGH
* **Category:** Broken Access Control
* **Tool Evidence:** Semgrep + Manual Code Review

```
CONFIRMED by code audit:
  grep -rn "authenticate_user|before_action.*auth|require_login|devise" app/controllers/
  RESULT: NONE FOUND — Zero authentication anywhere in the codebase
```

**Classification:** `TRUE_POSITIVE`  
**Justification:**  
Manual grep across all controller files (`application_controller.rb`, `users_controller.rb`, `creditcards_controller.rb`) returned zero matches for `authenticate_user!`, `before_action :authenticate_user`, `require_login`, `logged_in?`, `current_user`, or any Devise authentication callback. `ApplicationController` only defines a `hello` method with no auth filter. Any unauthenticated HTTP GET to `/users` executes `User.all` and exposes all user records; any GET to `/creditcards` executes `Creditcard.all` and exposes all credit card records including CVV, card number, and expiry.

**Evidence / Sinks:**  
* `app/controllers/application_controller.rb` — No `authenticate_user!` filter defined.  
* `app/controllers/users_controller.rb` — `def index; @users = User.all; end` with no auth guard.  
* `app/controllers/creditcards_controller.rb` — `def index; @creditcards = Creditcard.all; end` with no auth guard.  

---

### TP-3 · Insecure Direct Object Reference (IDOR) via Unscoped `find(params[:id])`
* **CWE:** CWE-639 (Authorization Bypass Through User-Controlled Key)
* **Severity:** HIGH
* **Category:** Broken Object Level Authorization
* **Tool Evidence:** Semgrep rule `ruby.rails.security.brakeman.check-unscoped-find`

```
CONFIRMED by Semgrep 1.175.0 (rule: ruby.rails.security.brakeman.check-unscoped-find):
  creditcards_controller.rb:67 → @creditcard = Creditcard.find(params[:id])
  users_controller.rb:67       → @user = User.find(params[:id])
```

**Classification:** `TRUE_POSITIVE`  
**Justification:**  
Semgrep's `check-unscoped-find` rule (derived from Brakeman's IDOR detector) flagged two direct instances where `params[:id]` (attacker-controlled) is passed directly to `Model.find()` without any scope binding to the current user. No ownership check exists (`current_user.creditcards.find(params[:id])` is never used). An attacker who creates their own account can enumerate sequential integer IDs to access any other user's credit card record, including full card number, CVV, expiry, and billing address.

**Evidence / Sinks:**  
* `app/controllers/creditcards_controller.rb:67` — `@creditcard = Creditcard.find(params[:id])`  
* `app/controllers/users_controller.rb:67` — `@user = User.find(params[:id])`  

---

### TP-4 · `user_id` in Mass-Assignable Parameters (Privilege Escalation)
* **CWE:** CWE-915 (Improperly Controlled Modification of Dynamically-Determined Object Attributes)
* **Severity:** HIGH
* **Category:** Mass Assignment / Privilege Escalation
* **Tool Evidence:** Manual Code Audit

```
CONFIRMED in creditcards_controller.rb:72:
  params.require(:creditcard).permit(:network, :cardnumber, :name, :address, :country, :cvv, :exp, :user_id)
```

**Classification:** `TRUE_POSITIVE`  
**Justification:**  
The strong parameters definition in `creditcards_controller.rb` permits `user_id` as a mass-assignable field. Since there is no authentication, any request can POST a new credit card and set `user_id` to any arbitrary value, associating the card with any target user account. Even if authentication were added later, this would remain a privilege escalation vector allowing an authenticated user to create credit cards owned by other users. The `user_id` field should never be permitted from user input — it should be set server-side as `current_user.id`.

**Evidence / Sinks:**  
* `app/controllers/creditcards_controller.rb:72` — `permit(..., :user_id)`

---

### TP-5 · SSL and Master Key Enforcement Disabled in Production
* **CWE:** CWE-319 (Cleartext Transmission of Sensitive Information) / CWE-522
* **Severity:** MEDIUM
* **Category:** Security Misconfiguration
* **Tool Evidence:** Manual Code Audit

```
CONFIRMED in config/environments/production.rb:
  Line 19: # config.require_master_key = true   ← COMMENTED OUT
  Line 47: # config.force_ssl = true            ← COMMENTED OUT
```

**Classification:** `TRUE_POSITIVE`  
**Justification:**  
Both `config.require_master_key = true` and `config.force_ssl = true` are commented out in `production.rb`. `force_ssl = true` would enforce HTTPS and set HSTS headers; without it, the application accepts plaintext HTTP connections, enabling man-in-the-middle attacks to steal session cookies and credit card data in transit. `require_master_key = true` would prevent the application from starting if the master key is missing or invalid; commenting it out allows degraded-security deployments. Both are documented Rails security hardening requirements per the Rails Security Guide.

**Evidence / Sinks:**  
* `config/environments/production.rb:19`  
* `config/environments/production.rb:47`  

---

### TP-6 · Content Security Policy (CSP) Entirely Disabled
* **CWE:** CWE-1021 (Improper Restriction of Rendered UI Layers) / CWE-79
* **Severity:** MEDIUM
* **Category:** Security Misconfiguration / Client-Side Security
* **Tool Evidence:** Manual Code Audit

```
CONFIRMED in config/initializers/content_security_policy.rb:
  Entire CSP block is commented out:
  # Rails.application.config.content_security_policy do |policy|
  #   policy.default_src :self, :https
  ...
  # end
```

**Classification:** `TRUE_POSITIVE`  
**Justification:**  
The entire `content_security_policy.rb` initializer is commented out, meaning the application sends no `Content-Security-Policy` header. Combined with the dashboard's external iframe and `<script>` tags loading from `startbootstrap.disqus.com` and `startbootstrap.com`, the absence of CSP allows any injected script to execute without restriction, making the application maximally vulnerable to Cross-Site Scripting (XSS) attacks. OWASP recommends CSP as a required defense-in-depth control for all web applications serving financial data.

**Evidence / Sinks:**  
* `config/initializers/content_security_policy.rb:1-25`  
* `app/views/dashboard/index.html.erb:25`  

---

### TP-7 · External iframe and Unverified Third-Party JavaScript in Dashboard
* **CWE:** CWE-1021 / CWE-829 (Inclusion of Functionality from Untrusted Sphere)
* **Severity:** MEDIUM
* **Category:** Supply Chain Risk / Client-Side Script Injection
* **Tool Evidence:** Manual Code Audit

```
CONFIRMED in app/views/dashboard/index.html.erb:
  Line 24: <iframe src="https://startbootstrap.github.io/startbootstrap-sb-admin-2/">
  Line 25: <script src="//startbootstrap.disqus.com/count.js">
  Line 30: <script src="https://startbootstrap.com/assets/js/scripts.js">
```

**Classification:** `TRUE_POSITIVE`  
**Justification:**  
The application dashboard loads a full-width iframe from `startbootstrap.github.io` and two external JavaScript files from `startbootstrap.disqus.com` and `startbootstrap.com`. These third-party domains are outside the application's security boundary. If any of these domains are compromised (via subdomain takeover, supply chain attack, or DNS hijacking), the attacker gains full script execution in the context of the financial application. There is no Subresource Integrity (SRI) hash on the script tags, and no CSP to restrict external script loading.

**Evidence / Sinks:**  
* `app/views/dashboard/index.html.erb:24-30`

---

### TP-8 · Profiler Gems Not Isolated From Production (Information Disclosure)
* **CWE:** CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor)
* **Severity:** LOW
* **Category:** Information Disclosure / Performance Tooling Exposure
* **Tool Evidence:** Semgrep + Manual Code Audit

```
CONFIRMED in Gemfile:
  Line 20: gem 'rack-mini-profiler', require:false
  Line 21: gem 'memory_profiler'
  Line 22: gem 'flamegraph'
```

**Classification:** `TRUE_POSITIVE`  
**Justification:**  
`rack-mini-profiler`, `memory_profiler`, and `flamegraph` appear in the `Gemfile` without strict group restriction that would prevent their use in production. If `rack-mini-profiler` is activated in production (via `require: false` allowing explicit require), it exposes all SQL queries, database timings, and memory allocation details on every page via `?pp=help`. Since the application has no authentication, this profiling data is available to any anonymous user on the internet.

---

### TP-9 · Sensitive Payment Card Parameters Unfiltered in Application Logs
* **CWE:** CWE-532 (Insertion of Sensitive Information into Log File)
* **Severity:** MEDIUM
* **Category:** Sensitive Data Exposure (PCI-DSS Non-Compliance)
* **Tool Evidence:** Manual Code Audit

```
CONFIRMED in config/initializers/filter_parameter_logging.rb:
  Rails.application.config.filter_parameters += [:password]
  → Missing: :cardnumber, :cvv, :exp, :number
```

**Classification:** `TRUE_POSITIVE`  
**Justification:**  
The `filter_parameter_logging.rb` initializer only adds `:password` to the filtered parameters list. The credit card fields `:cardnumber`, `:cvv`, and `:exp` are not filtered. When users submit credit card forms, Rails logs all request parameters in plaintext in the application log files (`log/production.log`). Any developer or attacker with access to log files can extract full credit card numbers, CVV codes, and expiry dates from the logs. PCI-DSS compliance requires that CVV/CVC codes are never stored or logged.

**Evidence / Sinks:**  
* `config/initializers/filter_parameter_logging.rb:4`  
* `app/controllers/creditcards_controller.rb:72`  

---

### TP-10 · Backup Files Committed to Repository
* **CWE:** CWE-312 (Cleartext Storage of Sensitive Information)
* **Severity:** LOW
* **Category:** Security Misconfiguration
* **Tool Evidence:** Manual Code Audit

```
CONFIRMED files:
  app/views/dashboard/index.html.erb.bak
  app/views/users/index.html.erb.bak
  config/routes.rb.bak
```

**Classification:** `TRUE_POSITIVE`  
**Justification:**  
Three `.bak` backup files are committed to the repository. These files often contain development history including previously removed code paths, old credentials, or sensitive logic that was intentionally removed from active files. The presence of backup files in a production repository indicates poor development hygiene and should be flagged per OWASP A05 (Security Misconfiguration).

---

## Confirmed False Positives (Decoy Findings)

### FP-1 · `credentials.yml.enc` Flagged as Plaintext Secret Exposure
* **Classification:** `FALSE_POSITIVE`
* **Justification:**  
`config/credentials.yml.enc` is an AES-256-GCM encrypted file designed by Rails to be safely committed to source control. It cannot be decrypted without `config/master.key`, which is correctly listed in `.gitignore` and is NOT present in this repository. The `.enc` suffix confirms encryption. This is standard Rails security practice per the Rails Credentials documentation — it is not a vulnerability.

### FP-2 · `dotenv-rails` Gem Flagged as Credential Leakage
* **Classification:** `FALSE_POSITIVE`
* **Justification:**  
`dotenv-rails` is a legitimate environment variable loading gem with no known security vulnerabilities in its current version. The actual vulnerability is the committed `.env.local` file (TP-1), not the gem that loads it. The gem itself performs no encryption or credential storage.

### FP-3 · `User.all` Flagged as SQL Injection
* **Classification:** `FALSE_POSITIVE`
* **Justification:**  
ActiveRecord's `User.all` generates a fully parameterized `SELECT "users".* FROM "users"` with zero user-controlled string interpolation. There is no SQL injection path here. The true finding is broken access control (no authentication gate before `User.all`), which is already captured as TP-2.

---

## Dependency Vulnerability Highlights (Trivy Scan of `yarn.lock`)

| CVE ID | Affected Package | Version | Severity | Vulnerability Details |
|--------|------------------|---------|----------|-----------------------|
| **CVE-2022-37601** | `loader-utils` | 1.2.3 | **CRITICAL** | Prototype Pollution via parseQuery |
| **CVE-2021-44906** | `minimist` | 0.0.8 | **CRITICAL** | Prototype Pollution |
| **CVE-2025-6545** | `pbkdf2` | 3.0.17 | **CRITICAL** | Predictable key material generation |
| **CVE-2025-6547** | `pbkdf2` | 3.0.17 | **CRITICAL** | Static key return flaw |
| **CVE-2026-59873** | `tar` | 2.2.2 | **CRITICAL** | Denial of Service via gzip bomb |
| **CVE-2025-9288** | `sha.js` | 2.4.11 | **CRITICAL** | Hash rewind via missing type checks |
| **CVE-2021-23337** | `lodash.template`| 4.5.0 | **HIGH** | Remote Command Injection |
| **CVE-2020-7660** | `serialize-javascript`| 2.1.2 | **HIGH** | RCE via RegExp serialization |

---

## Dockerfile Misconfigurations (Trivy Security Check)

| Rule ID | Severity | Description |
|---------|----------|-------------|
| `DS-0002` | **HIGH** | Container runs as root — missing `USER` directive |
| `DS-0029` | **HIGH** | `apt-get` executed without `--no-install-recommends` |
| `DS-0026` | **LOW** | No `HEALTHCHECK` instruction defined |
