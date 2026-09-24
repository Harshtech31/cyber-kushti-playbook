# DANGAL — WEB-01: Northwind Goods
> **Scenario type:** Web  
> **Deadline:** 24 Sep 2026, 11:00 PM IST  
> **Status:** NOT submitted — enter at 5 PM

---

## Quick Reference — What Happened

A financially motivated attacker exploited a chain of eight weaknesses across staging isolation,
session handling, authorisation, IDOR, SQL injection, race conditions, and an unsigned payment
callback handler to:
1. Steal a contractor's session via staging brute-force
2. Escalate to `internal_ops` on production
3. Exfiltrate 2.1 million customer records
4. Manufacture ₹1.91 crore in fraudulent store credit
5. Receive 4,118 orders worth of goods without paying

---

## Finding Classification — All 30 Findings

| # | One-line summary | CHAIN / DECOY | Reason |
|---|---|---|---|
| F1 | Attack surface monitor flags staging hostname public | **CHAIN** | Attacker discovers staging via certificate transparency |
| F2 | 4,118 reqs scan staging paths; GraphQL + schema = 200 OK | **CHAIN** | Reconnaissance maps the GraphQL endpoint |
| F3 | Staging GraphQL answers introspection; 214 ops exposed | **CHAIN** | Schema dump — attacker learns every operation incl. undecorated ones |
| F4 | Ticket to disable staging introspection closed "won't do" | context | Known accepted risk — explains why introspection was still on |
| F5 | 12,406 scanner events at prod edge, all blocked | **DECOY** | Authorized pentest vendor (confirmed by F6), never reached app |
| F6 | F5 traffic matches authorized pentest vendor exactly | **DECOY** | Proves F5 is legitimate scanning, not the attacker |
| F7 | 11 requests to staging GraphQL, 240–260 KB each on 23 Jul | **CHAIN** | Brute-force batch: large aliased recovery-code documents |
| F8 | Recovery code limit = 5 per *HTTP request*, not per operation in batch | **CHAIN** | The aliased batch bypass vulnerability |
| F9 | Recovery code cracked for D. Rathore staging account (on leave) | **CHAIN** | Attacker gains valid staging session for contractor account |
| F10 | Staging has NO GraphQL audit log (production-only) | **CHAIN** | Explains evidence gap — staging activity is forensically blind |
| F11 | Third role-grant op has no auth decorator (TODO comment) | **CHAIN** | Unprotected privilege escalation op deployed to production |
| F12 | Rathore's account sets `account_type=internal_ops` on production at 14:03 25 Jul | **CHAIN** | Privilege escalation executed on production |
| F13 | `internal_ops` grants order admin + bulk export access | **CHAIN** | Defines the blast radius of the escalation |
| F14 | 186,400 consecutive order ref lookups, 28 Jul – 30 Aug, scripted pattern | **CHAIN** | IDOR order enumeration — full customer record scrape |
| F15 | Order lookup has no ownership check on session vs order | **CHAIN** | The IDOR vulnerability enabling F14 |
| F16 | 2.14 GB sent to European hosting provider from 28 Jul | **CHAIN** | Data exfiltration confirmed — same host later sends fake callbacks |
| F17 | SQL UNION SELECT in product review submitted 4 Aug | **CHAIN** | Stored SQLi payload targeting the weekly merchandising report |
| F18 | Merchandising report (10 Aug): 2.1M rows vs 4,800 avg, written to shared object storage | **CHAIN** | SQLi triggered on report run — 2.1M records exfiltrated |
| F19 | 41,900 store credit entries = ₹1.91 cr; 38,200 by `svc:checkout` | **CHAIN** | Mass fraudulent store credit injected at scale |
| F20 | 1,190 entries: 8–40 credits on same order within 300 ms | **CHAIN** | Race condition exploited on store credit redemption |
| F21 | Profile update called 2,840 times with `store_credit_paise` key | **CHAIN** | Direct mass assignment of credit balances via unfiltered profile update |
| F22 | 4,118 callbacks with no gateway settlement, from European host IPs | **CHAIN** | Forged payment callbacks — same EU host as exfil (F16) |
| F23 | Callback handler skips HMAC verify when header is absent | **CHAIN** | The vulnerability enabling forged callbacks |
| F24 | Callback order refs are consecutive, real orders in `awaiting_payment` | **CHAIN** | Refs sourced from IDOR enumeration (F14); targets confirmed real |
| F25 | 51,388 injection events blocked at edge, global campaign | **DECOY** | Mass internet noise unrelated to this attacker; all blocked |
| F26 | `metabase-readonly` API token: approved ticket, scoped, allowlisted | **DECOY** | Fully legitimate token with governance trail — not attacker activity |
| F27 | 34 active tokens, 11 no expiry, 6 named departed staff | context | Hygiene issue but NOT a step in this specific kill chain |
| F28 | No anomalous staff sign-in in logs; Rathore's prod sign-in satisfied SSO+2FA | **CHAIN** | Session cookie portability — staging cookie used at production |
| F29 | Cookies scoped to parent domain, no env binding, accepted by both envs | **CHAIN** | The mechanism that makes staging session work on production |
| F30 | Staging: reachable, unmasked prod data, identical image, no owner | **CHAIN** | Confirms staging held real prod credentials to brute-force |

### Confirmed Decoys (exclude from kill chain)

| Finding | Why excluded |
|---|---|
| **F5** | Authorized pentest vendor; all blocked at edge; change ticket evidence in F6 |
| **F6** | Proof that F5 is authorized |
| **F25** | Global injection campaign; all blocked; edge auto-closed; no app errors |
| **F26** | Legitimate API token — proper change ticket, single scope, allowlisted |

---

## THE KILL CHAIN — 8 Steps

### Phase 1 — Reconnaissance

**Step 1 — Staging Discovery** `(F1 → F2 → F3)`

Attacker discovers staging API hostname resolves publicly (F1). Scans staging, gets 200 OK on the
GraphQL endpoint and schema route (F2). Fires an introspection query — staging returns all 214
operations, arguments and fields, including the undecorated role-grant operation and the unfiltered
profile update (F3).

---

### Phase 2 — Initial Access (23 July)

**Step 2 — Account Recovery Brute-Force via Batched Alias Bypass** `(F7 → F8 → F9)`

Target: D. Rathore's staging account (contractor on leave; real production data on staging via F30).

The rate limit on the six-digit recovery code is five failed attempts *per HTTP request*. The check
runs once before the document executes (F8). The GraphQL endpoint accepts arbitrarily many aliased
copies of the same mutation in a single document.

Attacker sends 11 HTTP requests of 240–260 KB each (F7), each containing thousands of aliased
recovery-code attempts. Effective attempts per request: uncapped. Recovery code cracked at 21:44
on 23 July; Rathore's staging session obtained (F9).

Evidence gap: staging has no GraphQL audit log (F10).

**Step 3 — Session Cookie Portability: Staging Session Used on Production** `(F29 → F28)`

Session cookies are scoped to the parent domain `northwind-goods.com` with no environment
component in the cookie name and no server-side binding to the issuing environment (F29). The
production API accepts a cookie issued by staging.

Attacker carries Rathore's staging session cookie to production. The production authentication log
confirms the 25 July production sign-in for Rathore used the same source address as the staging
activity — satisfying SSO and 2FA through the staging-issued cookie (F28).

---

### Phase 3 — Privilege Escalation (25 July)

**Step 4 — Mass Assignment Privilege Escalation to `internal_ops`** `(F11 → F12 → F13)`

Schema dump revealed the customer profile update operation accepts a free JSON merge of any keys
into the customer model, including `store_credit_paise`, `account_type`, and `email_verified` (from
environment section). No allowlist restricts permitted keys.

A third role-granting operation (F11) was added in May 2026 with no auth decorator — but this is
not needed here. The simpler path: attacker calls profile update with `account_type=internal_ops`
(F12). Operation succeeds. `internal_ops` grants access to order administration and the bulk export
function (F13).

---

### Phase 4 — Data Exfiltration (28 July – 10 August)

**Step 5 — IDOR Order Enumeration** `(F14 → F15 → F16)`

Order references are sequential (NW + nine digits) and printed on every invoice. The order lookup
endpoint authorises on session presence only — no ownership check (F15). Attacker runs 186,400
consecutive lookups from 48 rotating residential addresses in a scripted daytime-only pattern (F14).
Data flows to a European hosting provider: 2.14 GB from 28 July onward (F16).

**Step 6 — Stored SQL Injection via Product Review → Weekly Report** `(F17 → F18)`

On 4 August, attacker submits a product review containing a SQL UNION SELECT clause targeting the
customer table (F17). The merchandising report, run weekly by the data squad, composes its SQL by
string concatenation over review text (from environment section). On 10 August the report runs and
produces 2,100,441 rows against a normal weekly average of 4,800 (F18). Output written to a shared
object storage location readable by all 41 engineering staff and all partner developer accounts.
2.1 million customer records exfiltrated.

---

### Phase 5 — Fraud: Store Credit (August)

**Step 7 — Race Condition + Mass Assignment on Store Credit** `(F19 → F20 → F21)`

Two concurrent fraud mechanisms:

*Race condition (F20):* Store credit redemption reads the balance, subtracts the order total in
application code, and writes the new balance — no database row lock, no idempotency key. 1,190
orders show groups of 8–40 credit entries within 300 milliseconds: parallel redemption requests
each reading the pre-deducted balance, multiplying the credit.

*Mass assignment (F21):* Profile update called 2,840 times with `store_credit_paise` key, directly
writing arbitrary credit balances to customer accounts.

Combined result: ₹1.91 crore fraudulent store credit across 2,840 accounts (F19).

---

### Phase 6 — Fraud: Forged Payment Callbacks (22 August – 11 September)

**Step 8 — Unsigned Callback Forgery → Goods Shipped Without Payment** `(F22 → F23 → F24)`

The payment callback handler verifies HMAC signature when the header is present, but where the
header is absent it logs at debug level and proceeds — a 2023 branch added for a sandbox gateway
that did not sign its callbacks (F23). The debug log is not retained.

Attacker sends 4,118 forged POST callbacks from the same European hosting provider used for
exfiltration (F22, same host as F16). Each callback carries a real order reference harvested by
the IDOR enumeration in Step 5 (F24) — consecutive references corresponding to real orders in
`awaiting_payment` state. Each callback marks the order paid and releases it to the warehouse.
4,118 orders shipped; zero corresponding settlements from the gateway.

---

## Kill Chain Summary (Portal Entry Format)

```
Step 1 — STAGING RECON & SCHEMA DUMP
Attacker discovers staging hostname resolves publicly (F1). Scans staging; gets 200 OK on GraphQL
endpoint (F2). Introspection returns full 214-operation schema including undecorated operations and
mass-assignable profile fields (F3).

Step 2 — ACCOUNT RECOVERY BATCH-ALIAS BRUTE-FORCE (23 Jul)
Rate limit is 5 attempts per HTTP request, not per aliased operation. Attacker sends 11 HTTP
requests of ~250 KB each, each containing thousands of aliased recovery-code mutations (F7, F8).
Recovery code cracked for contractor D. Rathore's staging account at 21:44 (F9). Staging has no
GraphQL audit log (F10).

Step 3 — SESSION COOKIE PORTABILITY → PRODUCTION (25 Jul)
Session cookies scoped to parent domain with no environment binding; production accepts
staging-issued cookies (F29). Attacker carries Rathore's staging session to production (F28).

Step 4 — PRIVILEGE ESCALATION: MASS ASSIGNMENT → internal_ops (25 Jul)
Profile update accepts any JSON key including account_type. Attacker sets
account_type=internal_ops (F12). Grants order admin and bulk export access (F13).

Step 5 — IDOR ORDER ENUMERATION → EXFILTRATION (28 Jul – Aug)
Order refs are sequential. Order lookup has no ownership check (F15). 186,400 lookups enumerate
all customer order records (F14). 2.14 GB sent to European host (F16).

Step 6 — STORED SQL INJECTION VIA REVIEW → WEEKLY REPORT (4 Aug → 10 Aug)
Attacker submits a SQL UNION SELECT payload as a product review (F17). Merchandising report
concatenates review text into SQL; runs 10 Aug and returns 2.1 M rows (F18). 2.1 M customer
records written to shared object storage and exfiltrated.

Step 7 — STORE CREDIT FRAUD: RACE CONDITION + MASS ASSIGNMENT (Aug)
Race condition: no row lock on redemption; 1,190 orders show 8–40 credits within 300 ms (F20).
Mass assignment: profile update called 2,840 times with store_credit_paise key (F21). Total
fraudulent credit: ₹1.91 crore (F19).

Step 8 — FORGED UNSIGNED PAYMENT CALLBACKS → 4,118 ORDERS SHIPPED FREE (22 Aug – 11 Sep)
Callback handler skips HMAC verification when signature header is absent (F23). Attacker sends
4,118 forged callbacks from same European host (F22) using order references harvested by IDOR
(F24). Each marks an order paid; goods dispatched; no gateway settlement exists.
```

---

## Evidence Gaps (document for judges)

| Gap | Reason |
|---|---|
| Staging GraphQL activity details | Audit log production-only, staging blind (F10) |
| Callback signature presence | Payment callback log does not record header presence (F22) |
| Merchandising report SQL output | No object storage access logging (from controls section) |
| Store credit automation identity | `svc:checkout` actor unattributed |
