# CYBER KUSHTI 2026 - ROUND 3 KESARI OFFENSIVE CHEAT SHEET

> **RULE-DEPENDENT:** Kesari is publicly announced as a supervised assessment and presentation round, not a red-team exercise. Perform active testing only when the supplied scope permits it.

## Workflow

~~~text
Recon -> Architecture -> Surface -> Auth -> Authorization -> Input -> Logic -> Infrastructure -> Chains -> Proof -> Report
~~~

## First Pass: High-Yield Questions

1. Which roles, tenants, objects, and sensitive actions exist?
2. Does every server-side object action enforce ownership and role?
3. Can a request skip, repeat, reverse, or replay a business state?
4. Where does attacker-controlled input reach an interpreter, URL fetch, file path, template, query, or tool?
5. Which secrets, CI jobs, containers, cloud roles, or configs expand impact?
6. Can an LLM or retrieved content influence a privileged tool without independent authorization?

## Authorization Matrix

| Actor | Object/action | Expected | Actual | Evidence |
| --- | --- | --- | --- | --- |
| User A | own object read/update | allow |  |  |
| User A | User B object read/update | deny |  |  |
| User | admin route | deny |  |  |
| Admin | approved action | allow |  |  |
| Tenant A | Tenant B data | deny |  |  |

Test list, read, create, update, delete, export, approve, internal/admin routes, and asynchronous callbacks.

## Safe Tests

| Class | Minimal safe proof |
| --- | --- |
| Auth | compare unauthenticated, low-privilege, and expected-privilege outcomes |
| Authorization | change one object ID/tenant/role field at a time |
| Business logic | show one forbidden state transition or replay |
| Injection | harmless in-scope canary with source trace |
| SSRF | organiser-provided harmless destination only |
| Files | controlled non-executable sample and canonicalised path check |
| AI/tool use | benign tool request that must be rejected by server-side policy |

## Report Before Moving On

Record precondition, input/request, expected policy, actual result, source/data flow, impact, safe reproduction, cleanup, confidence, and recommended regression test.

## Stop Conditions

Stop when the test would be destructive, leave scope, expose a real secret, affect other competitors, or needs an organiser decision. Log the blocker rather than improvising.

