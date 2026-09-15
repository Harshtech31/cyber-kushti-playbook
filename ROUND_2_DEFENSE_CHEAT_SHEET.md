# CYBER KUSHTI 2026 - ROUND 2 DANGAL DEFENSE CHEAT SHEET

> **RULE-DEPENDENT:** the public announcement does not confirm a live defense/attack round. Use only if organiser instructions expressly authorise it.

## Before Attack

1. Verify scope, allowed controls, rollback path, and service-availability priority.
2. Save baseline: users, processes, services, listeners, connections, auth events, HTTP/API traffic, files/config, CPU/memory/disk.
3. Log known organiser and teammate activity. Mark expected ports, accounts, endpoints, destinations, and scheduled tasks.
4. Split work:
   - **M1:** Incident Commander, timeline, impact and availability decisions.
   - **M2:** host/application logs, auth, database, files/config.
   - **M3:** network, detection, containment execution and evidence.

## Detection Priorities

| Area | Look for |
| --- | --- |
| Authentication | failed/impossible logins, new users, privilege or token changes |
| Web/API | unfamiliar routes, parameter changes, bursts, enumeration, bypass attempts |
| Host | shells, unexpected processes, changed binaries, scheduled-task/service edits |
| Network | new listeners, outbound anomalies, scans, reverse connections, lateral movement |
| Database | mass reads, unusual privileged access, unexpected write/destructive queries |

## Incident Loop

~~~text
Detect -> Validate -> Scope -> Contain -> Eradicate -> Recover -> Verify -> Document
~~~

1. **Validate:** compare the signal with baseline and teammate log.
2. **Scope:** identify affected identity, host, route, data, and first/last known time.
3. **Contain:** use the narrowest reversible action first.
4. **Eradicate:** remove the confirmed cause, not merely the symptom.
5. **Recover:** restore known-good state and watch for recurrence.
6. **Verify:** repeat the original detection and service health checks.
7. **Document:** command/action, approver, time, result, and residual risk.

## Do Not Self-Inflict an Outage

- M1 approves any action that stops a service, deletes state, rotates shared credentials, or blocks broad traffic.
- Prefer token revocation, account disablement, route-specific filtering, and reversible isolation.
- Preserve evidence before modifying the affected state where that does not increase harm.
- A restart is not evidence of eradication.

## Final Notes

Keep a single incident timeline. Clearly separate confirmed fact, analyst inference, and unknown. Submit the shortest defensible story: detection, scope, containment, recovery, proof.

