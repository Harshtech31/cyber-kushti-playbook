# DANGAL — OT-02: Sundara Pharmaceuticals
> **Scenario type:** OT (Operational Technology)  
> **Deadline:** 24 Sep 2026, 11:00 PM IST  
> **Status:** NOT submitted — enter at 5 PM

---

## Quick Reference — What Happened

A supply-chain attacker compromised the Thermaxis autoclave vendor's corporate network, pivoted
through the site-to-site support tunnel into Sundara's plant network, and deployed unsigned
trojanized firmware onto autoclave 3. The firmware reported falsely good sterilisation parameters
to the process historian. Because the historian-to-batch-record integration account is exempt from
audit trail capture, no modification entries were created. A Qualified Person reviewed what appeared
to be a complete, compliant record and released a contaminated batch. Two hospitals in Germany
subsequently reported particulate matter in units from that batch.

The two main decoys are: background internet noise against the corporate firewall (F28) and the
clean corporate domain authentication log (F29), which only confirm the attacker did NOT use the
corporate path.

---

## Finding Classification — All 32 Findings

| # | One-line summary | CHAIN / DECOY | Reason |
|---|---|---|---|
| F1 | Site-to-site tunnel uses PSK from 2018, never rotated; authenticates site not individual | **CHAIN** | Weak tunnel auth — the attacker's physical entry path |
| F2 | Single shared account `thermaxis-svc` on appliance; no individual attribution possible | **CHAIN** | No accountability on the vendor path |
| F3 | Appliance log: 61 sessions in 365 days; no individual identity ever recorded | **CHAIN** | Explains attribution gap |
| F4 | Thermaxis confirmed own corporate compromise from ~July 2026; support infra in scope | **CHAIN** | Supply chain attack origin — explains how attacker got access to vendor tunnel |
| F5 | ISEM received Thermaxis breach notification Feb 2027; forwarded to IT desk, no action | context | Missed response — explains why Sundara didn't react; not a chain step itself |
| F6 | DMZ-to-autoclave segment firewall never configured to log | **CHAIN** | Explains evidence gap — no record of what the appliance reached |
| F7 | OPC UA endpoints on all 4 autoclaves: security policy None, anonymous auth | **CHAIN** | The vulnerability giving write access to any plant-network host |
| F8 | With None + anonymous: any host can read/write any OPC UA node without credentials | **CHAIN** | Explicitly confirms exploit is possible |
| F9 | Controllers accept firmware images without signature verification | **CHAIN** | Enables malicious firmware deployment |
| F10 | Autoclave 3 controller event log: 1 firmware update event, dated 2–5 Nov 2026 | **CHAIN** | Firmware update confirmed in the incident window |
| F11 | Autoclave 3 firmware hash doesn't match any Thermaxis build record | **CHAIN** | Trojanized firmware confirmed — not from legitimate vendor |
| F12 | Other 3 autoclaves run firmware matching Thermaxis records | context | Only autoclave 3 was targeted |
| F13 | Affected batch sterilised on autoclave 3 on 4 Nov 2026 | **CHAIN** | Links the trojanized controller to the released batch |
| F14 | Historian records autoclave 3 cycle as reaching required lethality, 41-min hold | **CHAIN** | The fabricated "good" data written by trojanized firmware |
| F15 | Preceding cycle ended 09:14, next began 10:02 — only 48 min available; 41+18=59 min needed | **CHAIN** | Proves the historian record is physically impossible — cycle was shorter |
| F16 | Heat up + equilibration + cooling = 18 min confirmed by 220 other cycles | **CHAIN** | Confirms the 18-min figure; the "hold" must have been ~30 min, not 41 |
| F17 | Time server on plant network: no auth, default credentials, accepts config from any host | **CHAIN** | Time manipulation vector to align fabricated timestamps |
| F18 | Time server log never enabled | **CHAIN** | Explains why time manipulation cannot be confirmed or ruled out |
| F19 | Batch record audit trail timestamps come from app server clock, which syncs to the time server | **CHAIN** | If time server was manipulated, all batch record timestamps are unreliable |
| F20 | `ebr-histlink` (historian → batch record integration) is EXEMPT from audit trail capture | **CHAIN** | The critical exemption: historian writes fabricated data with no modification entry created |
| F21 | Batch record complete, consistent, no modification entries between assembly and QP signature | **CHAIN** | Fabricated data appears authentic because of F20 exemption |
| F22 | QP's signature, review steps and timestamps all present and consistent | **CHAIN** | Legitimate sign-off on fabricated data — QP had no way to detect the fraud |
| F23 | Environmental monitoring for cleanroom on 4 Nov within limits, no anomaly | **DECOY** | Real unmanipulated data — confirms environment was fine; attack was on process data |
| F24 | Recipe transfer via unscanned removable media from engineering station | context | Potential attack vector but not the one used in this incident |
| F25 | Autoclave 3+4 engineering station runs EOL OS; not covered by endpoint detection | context | Possible lateral movement path; not proven to be used in this specific chain |
| F26 | Computer system validation records exist for all systems; no security testing in scope | context | Explains why OPC UA auth and firmware signing issues were not caught in validation |
| F27 | Sep 2026 regulatory inspection accepted exempt service accounts as "system accounts" | context | Explains why audit trail exemptions were never flagged by regulators |
| F28 | 140,000 refused corporate firewall attempts from 6,800 addresses, all refused | **DECOY** | Routine internet background noise; all refused; no plant access attempted this way |
| F29 | No anomalous corporate domain sign-ins in retained window | **DECOY** | Confirms attack did NOT come through corporate path; confirms plant/OT-only vector |
| F30 | 19 devices on autoclave segment; automation group can only identify 15 | context | Inventory gap; not a direct chain step |
| F31 | Appliance log: 4 sessions 2–5 Nov; Thermaxis service records show NO authorized activity | **CHAIN** | Proves those 4 sessions were unauthorized attacker access, not legitimate Thermaxis support |
| F32 | Contract: no per-individual identification required, no audit right over Thermaxis | context | Explains contractual failure to detect the Thermaxis-side breach |

### Confirmed Decoys (exclude from kill chain)

| Finding | Why excluded |
|---|---|
| **F23** | Environmental monitoring is real and clean — confirms attack was on process data, not physical environment |
| **F28** | Background internet noise hitting corporate firewall; all refused; unrelated to this incident |
| **F29** | Clean corporate auth log — *confirms* the attacker used the plant/OT path, not corporate |

---

## THE KILL CHAIN — 5 Steps

### Phase 1 — Supply Chain Initial Access

**Step 1 — Supply Chain Initial Access: Pivot Through Thermaxis VPN Tunnel** `(F4 → F1 → F2 → F31)`

Thermaxis's corporate network and customer support infrastructure were compromised from approximately
July 2026 (F4). Attacker leveraged the permanent, unrotated site-to-site IPsec tunnel established in
2018 (F1) to reach Sundara's DMZ vendor support appliance. Attacker authenticated using the shared
vendor account `thermaxis-svc` (F2), establishing 4 unauthorized support sessions between 2 and 5
November 2026 for which Thermaxis had zero scheduled or authorized service activities (F31).

---

### Phase 2 — Lateral Movement & Protocol Reconnaissance

**Step 2 — Lateral Movement to Autoclave Segment & Unauthenticated OPC UA Discovery** `(F6 → F7 → F8)`

From the DMZ support appliance, the attacker traversed the unmonitored firewall rule set into the
autoclave control segment (F6). Attacker enumerated the plant network and discovered that OPC UA server
endpoints across all four autoclave controllers were configured with security policy `None` and
anonymous user authentication (F7). This architectural misconfiguration allowed any host reaching the
endpoints to read and write arbitrary controller nodes without credentials or encryption (F8).

---

### Phase 3 — Malicious Firmware Deployment

**Step 3 — Unsigned Malicious Firmware Flashing on Autoclave 3 Controller** `(F9 → F10 → F11 → F12)`

The autoclave programmable controllers lacked cryptographic signature verification on incoming firmware
updates, accepting raw binary images sent over the support connection (F9). The attacker uploaded and
flashed an unauthorized, modified firmware image onto Autoclave 3's controller during the 2–5 November
access window, recorded as a single update event in the controller's overwritten event log (F10). The
resulting firmware hash matched no Thermaxis build record, while the other three autoclaves remained
on genuine vendor firmware (F11, F12).

---

### Phase 4 — Autonomous Process Telemetry Falsification

**Step 4 — Autonomous Process Telemetry Falsification by Trojanized Firmware** `(F13 → F14 → F15 → F16)`

During the production run on 4 November 2026 for the affected batch (F13), the trojanized firmware
abbreviated the physical sterilization hold cycle (to approximately 30 minutes) while autonomously
transmitting fabricated telemetry over OPC UA to the process historian, falsely reporting a full
41-minute hold phase and passing lethality metrics (F14). This fabricated report was physically
impossible: the preceding cycle ended at 09:14 and the next began at 10:02 (only 48 minutes total elapsed),
whereas a real 41-minute hold plus standard 18-minute heat-up/equilibration/cool-down requires at least
59 minutes (F15, F16).

---

### Phase 5 — Silent Batch Record Injection via Audit-Exempt Account

**Step 5 — Silent Batch Record Injection via Audit-Exempt Integration Account** `(F20 → F21)`

The process historian ingested the fabricated hold and lethality parameters from Autoclave 3 and
automatically committed them into the Electronic Batch Record (EBR) system using the integration service
account `ebr-histlink` (F20). Because `ebr-histlink` was configured as exempt from audit trail capture
(an exemption dating to 2019 to prevent automated entries from overwhelming the log), the falsified cycle
data was written directly into the legal batch record without generating any modification entries or audit
flags (F20). This produced a complete, internally consistent batch record showing every parameter in
specification without a single audit trail discrepancy (F21).

---

## Kill Chain Summary (Portal Entry Format)

```
Step 1 — SUPPLY CHAIN INITIAL ACCESS VIA THERMAXIS VPN TUNNEL (2–5 Nov) (F4 → F1 → F2 → F31)
Attacker pivots from compromised Thermaxis network (F4) through unrotated site-to-site IPsec tunnel
(F1) into DMZ vendor appliance. Authenticates with shared account thermaxis-svc (F2) across 4
unauthorized sessions (F31). Firewall logging disabled (F6).

Step 2 — LATERAL MOVEMENT & UNAUTHENTICATED OPC UA DISCOVERY (F6 → F7 → F8)
From DMZ appliance, attacker pivots into autoclave subnet (F6). Discovers OPC UA server endpoints on
all autoclave controllers configured with security policy None and anonymous authentication (F7),
allowing uncredentialed, unencrypted read/write access to controller nodes (F8).

Step 3 — UNSIGNED MALICIOUS FIRMWARE FLASHING ON AUTOCLAVE 3 (2–5 Nov) (F9 → F10 → F11 → F12)
Controllers accept firmware images without cryptographic signature verification (F9). Attacker flashes
trojanized firmware onto Autoclave 3 controller during 2–5 Nov window (F10). Firmware hash matches no
legitimate Thermaxis build (F11); other autoclaves unaffected (F12).

Step 4 — AUTONOMOUS PROCESS TELEMETRY FALSIFICATION VIA TROJANIZED FIRMWARE (4 Nov) (F13 → F14 → F15 → F16)
Affected batch sterilized 4 Nov (F13). Trojanized firmware shortens physical hold cycle but transmits
fabricated telemetry to process historian via OPC UA, reporting a 41-min hold and full lethality (F14).
Falsification is physically impossible: only 48 min available between cycles where 59 min is required
(41 + 18 min) (F15, F16).

Step 5 — SILENT BATCH RECORD INJECTION VIA AUDIT-EXEMPT INTEGRATION ACCOUNT (F20 → F21)
Historian writes fabricated cycle data into Electronic Batch Record system using service account
ebr-histlink (F20). Because ebr-histlink is exempt from audit trail capture, fabricated parameters are
committed with zero audit trail modification records, creating an ostensibly pristine batch record (F21).
```

---

## Evidence Gaps (document for judges)

| Gap | Reason |
|---|---|
| DMZ-to-autoclave segment network activity | Firewall rule set never configured to log (F6) |
| Which individual connected via thermaxis-svc | Shared account, no individual identity (F2, F3) |
| Time server manipulation | Time server log never enabled (F18) |
| What the attacker did between sessions | Controller event log overwrites after 200 events (F10) |
| Other autoclave segments reached | No plant network inventory or monitoring (F30) |

---

## Key Insight for Judges

The attack's genius is exploiting the intersection of three exemptions:
1. **Thermaxis tunnel authenticates the site** — once Thermaxis is compromised, the attacker is trusted
2. **OPC UA has no authentication** — the attacker writes to autoclave controllers freely
3. **`ebr-histlink` is audit-exempt** — falsified data flows into the batch record invisibly

The electronic signatures and audit trail the QP relies on are structurally sound — they record
what they are supposed to. The attack bypasses them by operating at the layer *below* the batch
record system, at the sensor-to-historian-to-EBR data flow, where no controls exist.
