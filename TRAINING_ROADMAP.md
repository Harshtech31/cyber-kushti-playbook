# CYBER KUSHTI 2026 - TRAINING ROADMAP

Use only legal labs, CTFs, intentionally vulnerable applications, or local practice targets. Each session ends with a one-page finding and a five-minute defense of the verdict.

| Week / topic | Concept | Lab | Expected skill | Success criteria | Common mistake |
| --- | --- | --- | --- | --- | --- |
| 1 - Authentication | identity, session, reset, JWT/OAuth | local intentionally vulnerable auth app | trace auth boundary | explain accepted/rejected flows | treating token decoding as validation |
| 2 - Authorization | IDOR/BOLA/BFLA, tenant isolation | multi-user API lab | build action matrix | prove one permitted/forbidden pair | testing only UI controls |
| 3 - Business logic | states, replay, concurrency | checkout/approval workflow lab | state diagram | show forbidden transition safely | scanner-only review |
| 4 - API security | schemas, mass assignment, webhooks | REST/GraphQL/WebSocket lab | controlled request comparison | document server policy gap | changing many variables at once |
| 5 - SSRF and injection | input-to-sink / outbound trust | local training target | source trace + harmless proof | distinguish reachable from theoretical | unsafe payload escalation |
| 6 - Files and secrets | upload/download, config, credential capability | local upload + repo history lab | redact and assess impact | correct secret verdict | reporting every key-shaped string |
| 7 - Containers/cloud/CI | identity, images, IaC, pipeline trust | sample Docker/IaC repo | map deployment path | find a real config risk | assuming Dockerfile equals production |
| 8 - AI security | prompt injection, RAG, tool/MCP auth | local tool-calling/RAG demo | model tool boundary | prove server-side authorization need | trusting model intent |
| 9 - Incident response | baseline, triage, containment | synthetic logs/process/network scenario | incident timeline | narrow, reversible containment | restarting before collecting facts |
| 10 - Mock competition | all handoffs and reporting | 60-120 minute package | team rhythm | clean assessment defense | everyone chasing same issue |

## Session Pattern

1. **20 min** individual discovery.
2. **20 min** source/data-flow validation by Member 2.
3. **15 min** safe proof by Member 3.
4. **15 min** impact/severity/chain review by Member 1.
5. **10 min** report and oral defense.
6. **5 min** record one improvement.

## Suggested Legal Practice Sources

- OWASP Juice Shop, WebGoat, DVWA, and intentionally vulnerable local APIs.
- PortSwigger Web Security Academy for web security practice.
- OWASP WebGoat and OWASP security testing guidance for structured exercises.
- Vendor or platform labs only under their stated terms.

## Progress Gate Before Competition

The team should be able to take one scanner alert, prove or reject it with source reasoning, safely validate it where authorised, write a concise finding, and defend both the verdict and severity in under 15 minutes.

