# DANGAL — SUP-01: Anvil Systems
> **Scenario type:** Supply chain  
> **Deadline:** 24 Sep 2026, 11:00 PM IST  
> **Status:** NOT submitted — enter at 5 PM

---

## Quick Reference — What Happened

A threat actor compromised Anvil Systems — a UK-based industrial control systems integrator —
through a spear-phishing email targeting a privileged engineer. They established persistence, moved
laterally to the build environment, trojanised the update package for Anvil's flagship SCADA
product (Meridian SCADA), and shipped it through the legitimate signed update channel to over
200 of Anvil's industrial customers. The malicious update contained a time-delayed payload that
activated on a specific date, causing process disruptions at the manufacturing plants that had
installed it. Anvil's own code signing key was used, making the update indistinguishable from
legitimate software on signature alone.

---

## Finding Classification — All 30 Findings

| # | One-line summary | CHAIN / DECOY | Reason |
|---|---|---|---|
| F1 | Phishing email on 3 Jan 2027 to B. Okafor (solutions architect); contained weaponised document | **CHAIN** | Initial access vector |
| F2 | Okafor opened the document; corporate EDR recorded a malicious macro execution; alert auto-closed by tuning rule | **CHAIN** | Execution confirmed; missed detection due to alert suppression |
| F3 | 14 minutes after macro execution: encoded PowerShell beacon to a cloud provider address | **CHAIN** | C2 established post-execution |
| F4 | EDR alert auto-closed by a tuning rule created in October 2026 to reduce noise from a legitimate admin tool that used similar PowerShell encoding | **CHAIN** | Explains the missed detection; tuning rule is too broad |
| F5 | Okafor is a solutions architect with admin rights on six engineering workstations and read access to the product build share | **CHAIN** | Defines the blast radius of the initial compromise |
| F6 | Lateral movement on 17 Jan: Okafor's credentials used on build-srv-01 (the SCADA build server) | **CHAIN** | Pivot to the build environment using stolen/compromised credentials |
| F7 | Build-srv-01 runs the SCADA product build pipeline; finished binaries written to a release drop share | **CHAIN** | Confirms the build server is the target for supply chain poisoning |
| F8 | On 19 Jan: two new scheduled tasks on build-srv-01 under the SYSTEM account; names mimic Windows maintenance tasks | **CHAIN** | Persistence established on the build server |
| F9 | Scheduled tasks execute an encoded PowerShell script from a path under ProgramData that existed on no prior baseline image | **CHAIN** | Malicious payload executing on build server |
| F10 | On 22 Jan: Meridian SCADA v4.2.1 build was initiated and completed. The build log shows the standard pipeline steps. | **CHAIN** | The trojanised build |
| F11 | A diff of v4.2.1 against v4.2.0 shows one additional DLL (telemetry-helper.dll) not present in the source repo and not added by any build pipeline step | **CHAIN** | The trojanised component — injected outside the source control |
| F12 | telemetry-helper.dll is loaded by the Meridian SCADA service at startup via a manifest entry added to the service configuration in the build | **CHAIN** | Persistence mechanism for the malicious DLL |
| F13 | The DLL contains a date-triggered payload: dormant until 15 March 2027, then reads process tags and writes modified values to the same tags | **CHAIN** | The time-delayed sabotage payload |
| F14 | Anvil holds an EV code signing certificate. All release packages are signed before being pushed to the update server | **CHAIN** | The attacker's advantage: build server had signing access → package legitimately signed |
| F15 | Update pushed to the Anvil update server on 23 Jan; 214 customer instances pulled the update via auto-update | **CHAIN** | Delivery at scale — 214 customers received the trojanised update |
| F16 | 47 customers had auto-update disabled; they received manual notification on 23 Jan but are not in scope of F15 | context | Defines the auto-update population; not part of the attack chain itself |
| F17 | The Meridian SCADA update server performs no behavioural validation; it checks only that the package carries a valid Anvil signature | context | Explains why the check was passed — not an attacker step |
| F18 | On 15 March at 00:00, 198 of the 214 auto-updated instances activated the payload (16 were offline or unpatched to v4.2.1 by then) | **CHAIN** | Payload activation — simultaneous disruption at scale |
| F19 | Activation caused incorrect process setpoints to be written; at 26 of those sites automated safety systems tripped correctly and shut down affected equipment | **CHAIN** | Confirms industrial impact at 26 sites; safety systems functioned |
| F20 | At 3 sites safety systems did not trip; process ran outside safe parameters for between 4 and 19 minutes before operators intervened | **CHAIN** | Physical harm at 3 sites — most severe outcome |
| F21 | Anvil's update verification procedure: QA engineer reviews release notes and checks the package signature; no binary diff against previous release, no static analysis | context | Explains why the additional DLL was not caught in QA |
| F22 | HR records show Okafor attended a phishing awareness training on 14 November 2026, seven weeks before the incident | context | Background — awareness training did not prevent the compromise |
| F23 | The EDR tuning rule that suppressed F2's alert was created by a senior engineer following a helpdesk ticket; it was not peer reviewed | **CHAIN** | Explains the governance failure that allowed the alert suppression |
| F24 | Build-srv-01 is not enrolled in the endpoint agent; it is a validated build environment and the security team accepted it as an exception in 2024 | **CHAIN** | Explains why EDR telemetry was absent on the build server itself |
| F25 | The build pipeline has no integrity check comparing compiled output binaries against source-derived artefacts | **CHAIN** | The missing control that would have caught the injected DLL |
| F26 | Source control shows no commit adding telemetry-helper.dll or modifying the service manifest between v4.2.0 and v4.2.1 | **CHAIN** | Confirms the DLL was injected post-build, outside source control |
| F27 | A security researcher submitted a responsible disclosure on 28 February 2027 noting that Meridian SCADA v4.x lacked ASLR on several DLLs | **DECOY** | Legitimate independent disclosure about a different issue; unrelated to this attack |
| F28 | Anvil's incident response retainer was invoked on 16 March 2027; the retainer requires 4-hour response and forensic capability | context | Response process — not a chain step |
| F29 | Anvil's software composition analysis tool flagged three open source libraries in v4.2.0 as having known CVEs; these were unrelated to the attack | **DECOY** | Legitimate SCA finding — different issue; not part of this kill chain |
| F30 | Network flow logs from the Anvil corporate network between 3 January and 22 January show 18 GB of outbound traffic to a cloud provider address that corresponds to the C2 from F3; this destination had zero prior traffic history | **CHAIN** | Confirms C2 active and data exfiltration / command traffic over 3 weeks |

### Confirmed Decoys (exclude from kill chain)

| Finding | Why excluded |
|---|---|
| **F27** | Independent researcher disclosure about ASLR — completely unrelated to DLL injection attack |
| **F29** | SCA tool CVE findings in open source libraries — different issue, not part of this attack chain |

---

## THE KILL CHAIN — 7 Steps

### Phase 1 — Initial Access (3 January 2027)

**Step 1 — Spear Phish → Macro Execution → C2 Beacon** `(F1 → F2 → F3 → F4 → F30)`

Attacker sends a weaponised document to B. Okafor (solutions architect) on 3 January (F1). Okafor
opens it; corporate EDR records a malicious macro execution (F2). An alert fires — but it is
auto-closed by a tuning rule created in October 2026 to reduce noise from a legitimate admin tool
that used similar PowerShell encoding (F4). The tuning rule was not peer-reviewed (F23).

14 minutes post-execution, an encoded PowerShell beacon calls out to a cloud provider address (F3).
Network flows confirm 18 GB outbound to that address over 3–22 January (F30) — C2 established
and maintained.

---

### Phase 2 — Privilege and Lateral Movement (17 January)

**Step 2 — Okafor's Credentials → Build Server Pivot** `(F5 → F6 → F7)`

Okafor holds admin rights on 6 engineering workstations and read access to the product build share
(F5). On 17 January, the attacker uses Okafor's credentials to authenticate to `build-srv-01` —
the SCADA product build server (F6). The server runs the Meridian SCADA build pipeline and writes
finished binaries to the release drop share (F7).

Build-srv-01 is not enrolled in the EDR endpoint agent — accepted as an exception in 2024 for a
validated build environment (F24). No EDR telemetry exists for activity on the server itself.

---

### Phase 3 — Persistence on Build Server (19 January)

**Step 3 — Scheduled Tasks for Persistence** `(F8 → F9)`

On 19 January, two scheduled tasks are created on `build-srv-01` under the SYSTEM account. Names
mimic Windows maintenance tasks (F8). Tasks execute an encoded PowerShell script from a
ProgramData path that appears on no prior baseline image (F9). Persistence secured on the build
server.

---

### Phase 4 — Build Poisoning (22 January)

**Step 4 — DLL Injection Into SCADA Build** `(F10 → F11 → F12 → F13 → F25 → F26)`

On 22 January the Meridian SCADA v4.2.1 build runs through the standard pipeline (F10). Outside
the source-controlled pipeline, the attacker injects `telemetry-helper.dll` into the compiled
output — the DLL appears in no source repository commit between v4.2.0 and v4.2.1 (F26). The
build pipeline has no integrity check comparing compiled output against source-derived artefacts
(F25), so the injection passes undetected.

The DLL is loaded by the Meridian SCADA service at startup via a manifest entry added to the
service configuration during the build (F12). It contains a date-triggered payload: dormant until
15 March 2027, then reads process tags and writes modified values back to them (F13).

---

### Phase 5 — Signed Delivery (23 January)

**Step 5 — Legitimate Code Signing → Update Server → 214 Customers** `(F14 → F15)`

Anvil's release process signs all packages with its EV code signing certificate before pushing to
the update server (F14). The trojanised v4.2.1 package carries a valid Anvil signature —
indistinguishable from a legitimate release. On 23 January the package is pushed to the update
server; 214 customer instances pull it via auto-update (F15). Anvil's QA review checks the
signature and reads the release notes but performs no binary diff against the previous release
and no static analysis (F21).

---

### Phase 6 — Payload Activation (15 March 2027)

**Step 6 — Time-Triggered Payload Activates at 200 Sites** `(F13 → F18 → F19 → F20)`

At 00:00 on 15 March 2027, the dormant payload activates on 198 of the 214 auto-updated instances
(16 were offline or had rolled back by then) (F18). The payload writes incorrect process setpoints
to live SCADA tags simultaneously across all activated instances.

At 26 sites, automated safety systems function correctly and trip the equipment (F19). At 3 sites,
safety systems do not trip; process runs outside safe parameters for 4 to 19 minutes before
operators intervene (F20). Physical harm at scale.

---

## Kill Chain Summary (Portal Entry Format)

```
Step 1 — INITIAL ACCESS: SPEAR PHISH → MACRO → C2 (3 Jan 2027) (F1 → F2 → F3)
Weaponised document sent to B. Okafor (solutions architect, admin rights on 6 workstations).
Okafor opens it; macro executes (F2). EDR alert auto-closed by an unreviewed tuning rule (F4, F23).
Encoded PowerShell C2 beacon fires 14 min later (F3). 18 GB outbound C2 traffic 3–22 Jan (F30).

Step 2 — LATERAL MOVEMENT TO BUILD SERVER (17 Jan) (F5 → F6 → F7)
Okafor's credentials used to authenticate to build-srv-01 (F6) — the Meridian SCADA build server.
Build-srv-01 not in EDR (accepted exception 2024, F24). No endpoint telemetry for on-box activity.

Step 3 — PERSISTENCE ON BUILD SERVER (19 Jan) (F8 → F9)
Two SYSTEM-level scheduled tasks created with Windows-maintenance-style names (F8). Execute
encoded PowerShell from a ProgramData path absent from all baseline images (F9).

Step 4 — DLL INJECTION INTO SCADA BUILD (22 Jan) (F10 → F11 → F12 → F13)
Meridian SCADA v4.2.1 built through standard pipeline. Attacker injects telemetry-helper.dll
into compiled output outside source control (F11, F26). Build pipeline has no binary integrity
check (F25). DLL loads at service startup via manifest entry (F12). Contains time-triggered
payload: dormant until 15 Mar 2027 then modifies process tags (F13).

Step 5 — SIGNED DELIVERY TO 214 CUSTOMERS (23 Jan) (F14 → F15)
Package signed with Anvil's EV code signing certificate (F14) — legitimate signature. Pushed to
update server; 214 customer instances auto-update. QA checks signature only, no binary diff (F21).

Step 6 — PAYLOAD ACTIVATION: SIMULTANEOUS DISRUPTION AT 200 SITES (15 Mar 2027) (F18 → F19 → F20)
At 00:00 on 15 Mar, payload activates on 198 instances. Incorrect process setpoints written to
live SCADA tags simultaneously. Safety systems trip at 26 sites (F19). At 3 sites safety systems
fail to trip; process runs outside safe parameters 4–19 min (F20).
```

---

## Evidence Gaps

| Gap | Reason |
|---|---|
| On-box activity on build-srv-01 | No EDR agent (accepted exception, F24) |
| How DLL was staged for injection | No EDR on build server; F30 confirms C2 but not specific file transfers |
| Full scope of data exfiltration in 18 GB | C2 traffic confirmed but no DLP or content inspection |
| Which 3 sites had safety system failures | Not stated in findings — regulatory disclosure issue |
