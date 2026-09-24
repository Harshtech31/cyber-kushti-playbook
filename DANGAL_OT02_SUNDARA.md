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

**Step 1 — Thermaxis Corporate Compromise → Vendor Tunnel** `(F4 → F1 → F2 → F31)`

Thermaxis's corporate network, including customer support infrastructure, was compromised from
approximately July 2026 (F4). Attacker gains access to Thermaxis's network and from it initiates
the site-to-site tunnel to Sundara (F1 — PSK from 2018, never rotated, authenticates site not
individual). Logs into the vendor appliance as `thermaxis-svc` (F2 — single shared account, no
individual identity possible).

The appliance session log records 4 sessions between 2 and 5 November 2026 (F31). Thermaxis's
own service records show no scheduled or unscheduled support activity for Sundara in that period.
These 4 sessions are the unauthorized attacker sessions.

The DMZ-to-autoclave segment firewall has no logging enabled (F6) — no record of what the
appliance reached or when.

---

### Phase 2 — Trojanized Firmware Deployment

**Step 2 — Write Unsigned Firmware to Autoclave 3 via OPC UA** `(F7 → F8 → F9 → F10 → F11)`

From the vendor appliance, attacker reaches autoclave 3's controller on the autoclave segment.
OPC UA is configured with security policy None and anonymous authentication on all four autoclaves
(F7). With this configuration, any host able to reach the endpoint can read or write any node
without credentials; traffic is unencrypted and unprotected (F8).

Autoclave controllers accept firmware images without signature verification (F9). Attacker
deploys a trojanized firmware image. The controller event log records one firmware update event
dated to the 2–5 November window (F10). The firmware running on autoclave 3 on 18 March does
not match any Thermaxis build record (F11) — it was not issued by the legitimate vendor.

---

### Phase 3 — Process Data Falsification

**Step 3 — Trojanized Firmware Reports False Sterilisation Parameters** `(F13 → F14 → F15 → F16)`

The affected batch is sterilised on autoclave 3 on 4 November 2026 (F13). The trojanized firmware
reports a hold phase of 41 minutes and sufficient accumulated lethality to the process historian (F14).

This is physically impossible: the preceding cycle on autoclave 3 ended at 09:14 and the following
cycle began at 10:02 — only 48 minutes available. A 41-minute hold plus the documented 18 minutes
of heat-up, equilibration and cooling (F16 — consistent across 220 other cycles) requires 59 minutes
(F15). The actual hold phase was at most approximately 30 minutes — insufficient for the required
lethality.

The historian faithfully records the false values reported by the controller.

---

### Phase 4 — Audit Trail Bypass → Batch Record Fabrication

**Step 4 — Historian Writes Fabricated Data via Audit-Exempt Account** `(F20 → F21 → F22)`

The process historian writes cycle data into the electronic batch record via the service account
`ebr-histlink`. This account is configured as exempt from audit trail capture — exempted in 2019
so routine automated inserts would not overwhelm the trail (F20). The exemption means historian
writes create no modification entries in the audit trail, regardless of what values are written.

The batch record assembles with the historian's falsified parameters. The record is complete,
internally consistent, and shows every parameter within specification. The audit trail contains no
modification entries of any kind between assembly and QP signature (F21).

Optional time alignment: the plant-wide time server has no authentication and accepts configuration
over HTTP with vendor default credentials (F17). If the timestamps needed adjustment, the attacker
could have shifted the time server to align all clock-derived timestamps (F18, F19) — the time
server log was never enabled so this cannot be confirmed or denied.

**Step 5 — Qualified Person Releases Contaminated Batch** `(F22)`

The Qualified Person reviews the assembled batch record. The signature, the review steps and the
timestamps are all present and consistent (F22). The QP has no mechanism to detect that the
process parameters were reported by trojanized firmware or that the historian integration is
exempt from audit trail capture. The QP releases the batch.

Contaminated product ships to regulated markets. In March 2027, two units from the batch show
visible particulate matter in a German hospital pharmacy, triggering recall and regulatory
notification.

---

## Kill Chain Summary (Portal Entry Format)

```
Step 1 — SUPPLY CHAIN: THERMAXIS COMPROMISE → VENDOR TUNNEL → PLANT ACCESS (Nov 2026)
Thermaxis corporate network compromised from ~Jul 2026; support infrastructure in scope (F4).
Attacker connects through site-to-site tunnel (PSK from 2018, never rotated, site auth only) (F1).
Logs into vendor appliance as shared account thermaxis-svc (F2). 4 sessions 2–5 Nov recorded in
appliance log (F31); Thermaxis records show no authorized activity in that period. DMZ firewall
not logging — no record of what was reached (F6).

Step 2 — TROJANIZED FIRMWARE ON AUTOCLAVE 3 VIA UNAUTHENTICATED OPC UA (2–5 Nov)
OPC UA configured with security policy None and anonymous auth on all autoclaves (F7, F8).
Any host on plant network can write any node without credentials. Controllers accept unsigned
firmware (F9). Attacker deploys trojanized firmware to autoclave 3. Controller event log records
firmware update 2–5 Nov (F10); firmware hash matches no Thermaxis build record (F11).

Step 3 — FIRMWARE FALSIFIES STERILISATION PARAMETERS TO HISTORIAN (4 Nov)
Affected batch sterilised on autoclave 3 on 4 Nov (F13). Trojanized firmware reports 41-min hold
and required lethality to historian (F14). Physically impossible: only 48 min between cycles;
41+18 min required = 59 min (F15, F16). Actual hold ~30 min — insufficient lethality.
Historian records the fabricated values faithfully.

Step 4 — AUDIT-EXEMPT HISTORIAN ACCOUNT WRITES FALSE DATA → NO MODIFICATION ENTRY (4 Nov)
Historian writes to batch record via ebr-histlink, which is exempt from audit trail capture (F20).
Fabricated parameters enter the batch record with zero audit trail evidence. Record appears
complete, consistent, all parameters within specification (F21).

Step 5 — QUALIFIED PERSON RELEASES CONTAMINATED BATCH (Nov 2026)
QP reviews assembled record; signature, review steps and timestamps all present and consistent (F22).
No mechanism to detect firmware falsification or audit trail exemption. Batch released. Contaminated
product ships to regulated markets. Particulate matter reported in Germany, Mar 2027.
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
