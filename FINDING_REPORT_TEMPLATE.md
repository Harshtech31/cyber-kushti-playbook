# CYBER KUSHTI 2026 - FINDING / REPORT TEMPLATES

Use **Template A** for confirmed vulnerabilities (True Positives).  
Use **Template B** for debunked alerts / AI hallucinations (False Positives).

---

## TEMPLATE A: TRUE POSITIVE FINDING (CONFIRMED)

```text
================================================================================
FINDING ID: SEC-XXX
TITLE: [Concise title: Vulnerability Type in Component / Endpoint]
VERDICT: TRUE POSITIVE
SEVERITY: Critical / High / Medium / Low
DISCOVERY SOURCE: AI Prompt / Semgrep / CodeQL / Gitleaks / Trivy / Manual Logic Audit
AFFECTED COMPONENT: [e.g. Auth Service / Checkout API / User Profile]
ENDPOINT / ROUTE: [e.g. POST /api/v1/orders/{order_id}/refund]
CODE LOCATION: [e.g. src/controllers/orderController.js: lines 42-68]
TARGET COMMIT: [e.g. git rev-parse HEAD]
OWNER: [M1 / M2 / M3]
================================================================================

1. VULNERABILITY SUMMARY:
[1-2 clear sentences explaining the underlying defect and practical exploit consequence.]

2. PRECONDITIONS & ATTACK VECTOR:
- Threat Actor: [Unauthenticated / Low-Privilege User / Tenant A]
- Attacker Input: [Exact JSON field, query param, HTTP header, or file payload]
- Prerequisites: [e.g. Valid user session or network access to port 8080]

3. STATIC ANALYSIS EVIDENCE (CODE DATA FLOW):
- Source (Entry): [File:Line - where untrusted input enters the application]
- Intermediate Processing: [File:Line - transforms, missing or flawed checks]
- Sensitive Sink: [File:Line - SQL execute / exec / file write / state mutation]
- Vulnerable Code Snippet:
  ```
  [Paste 5-10 relevant lines of code from target repo]
  ```

4. DYNAMIC ANALYSIS EVIDENCE (RUNTIME / HTTP / LOGS):
- Reproduction Request (curl / HTTPie):
  ```bash
  curl -i -X POST http://localhost:8080/api/v1/orders/102/refund \
    -H "Authorization: Bearer <USER_A_TOKEN>" \
    -H "Content-Type: application/json" \
    -d '{"amount": 5000}'
  ```
- Observed Response:
  ```http
  HTTP/1.1 200 OK
  Content-Type: application/json

  {"status":"refunded","order_id":102,"amount":5000}
  ```
- Application / Container Log Confirmation:
  ```text
  [2026-09-15 18:24:12] INFO: Processing refund for order 102 by user 45 (Unauthorized Owner)
  ```

5. DEMONSTRATED BUSINESS & SECURITY IMPACT:
- Data / Asset Affected: [e.g. Financial loss, unauthorized access to Tenant B records]
- Scope of Breach: [e.g. Any authenticated user can trigger refunds for any order ID]
- Attack Chain Potential: [e.g. Can be chained with SEC-003 to drain account balances]

6. REMEDIATION (ROOT CAUSE FIX):
- Specific Fix:
  [Describe exact code change needed - e.g. enforce tenant ownership check in SQL query]
- Remediated Code Diff:
  ```diff
  - const order = await Order.findById(orderId);
  + const order = await Order.findOne({ _id: orderId, userId: req.user.id });
  + if (!order) return res.status(404).json({ error: "Order not found or unauthorized" });
  ```

7. REGRESSION TEST:
- Verification Test:
  [Exact automated test or curl assertion that returns 403/404 after fix]

8. SIGN-OFF GATE:
- M1 Impact & Severity Approval: [Initials / Timestamp]
- M2 Static Code Proof Approval: [Initials / Timestamp]
- M3 Dynamic Reproduction Approval: [Initials / Timestamp]
```

---

## TEMPLATE B: FALSE POSITIVE JUSTIFICATION (DEBUNKED ALERT)

```text
================================================================================
ALERT ID: FP-XXX (or original Scanner/AI ID)
TITLE: [Claimed Vulnerability: e.g. SQL Injection in Search Controller]
VERDICT: FALSE POSITIVE
ORIGINAL SOURCE: AI Prompt / Semgrep Rule / CodeQL / Dependabot / Trivy
CLAIMED SEVERITY: Critical / High
AFFECTED COMPONENT: [e.g. Search Module]
CODE LOCATION: [e.g. src/services/searchService.py: line 88]
OWNER: [M2 / M3]
================================================================================

1. CLAIMED DEFECT:
[What did the scanner or AI hallucinate/claim was vulnerable?]

2. TECHNICAL DEBUNK & ROOT CAUSE OF ERROR:
[Why is this claim definitively false? Select applicable technical reality:]
- [ ] Non-Attacker Input: Input originates from server-controlled configuration or hardcoded constants.
- [ ] Safe Parameterization: ORM / DB driver safely binds variables at runtime despite string concatenation appearance.
- [ ] Framework Auto-Sanitization / Escaping: Modern template engine automatically escapes output context.
- [ ] Dead / Unreachable Code: Function is never imported, route is unmounted, or file is a test/mock fixture.
- [ ] Compensating Server-Side Control: Upstream middleware strictly enforces schema/type allowlists.
- [ ] Dev / Build-Time Dependency Only: Package is not packaged or deployed to the production runtime.

3. CODE-GROUNDED EVIDENCE (STATIC PROOF OF SAFETY):
- File & Line Reference: [src/services/searchService.py: line 88]
- Code Snippet Showing Compensating Control / Safe Implementation:
  ```python
  # Code showing safe prepared statement or type enforcement
  ```
- Call-Site Proof (if unreachable/dead code):
  ```bash
  # ripgrep output proving function is uncalled in production routes
  rg "search_internal_debug" src/
  ```

4. DYNAMIC VALIDATION PROOF (IF APPLICABLE):
- Test Request Sent:
  ```bash
  curl -i "http://localhost:8080/api/search?q='OR+1=1--"
  ```
- Observed Runtime Defense:
  ```http
  HTTP/1.1 400 Bad Request
  {"error": "Invalid character in search query. Alphanumeric only."}
  ```

5. CONCLUSION:
[1 clear sentence explaining why judges should discard this finding and award points for identifying a false alarm.]

6. SIGN-OFF:
- M2 Code Verification: [Initials]
- M3 Runtime Verification: [Initials]
```

---

## Standard for Reporting Quality

1. **Be Exact**: Always cite file name, function name, and line numbers.
2. **Redact Sensitive Material**: Never put raw production secrets or uncontrolled binary payloads in reports.
3. **No Blind Trust**: Never paste raw AI explanations or raw Semgrep JSON directly into the final report. Translate into human, defensible technical conclusions.


