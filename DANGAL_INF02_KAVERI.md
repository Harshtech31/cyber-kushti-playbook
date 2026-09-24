# DANGAL — INF-02: Kaveri Broadcast Network
> **Scenario type:** Infrastructure  
> **Deadline:** 24 Sep 2026, 11:00 PM IST  
> **Status:** NOT submitted — enter at 5 PM

---

## Quick Reference — What Happened

A threat actor gained initial access through an unmanaged network printer (vendor default password),
extracted service account credentials stored on the device, used those credentials to pivot into
the media asset management system and newsroom file share (data theft), then abused the SNMP
write community string to reconfigure switch ports and take all four broadcast channels off air.
Building automation was also disabled, causing thermal damage risk in the Chennai rack room. The
attacker claimed access since January 2027. 1,327 unmanaged devices were entirely invisible to
every compliance and security control.

---

## Finding Classification — All 32 Findings

| # | One-line summary | CHAIN / DECOY | Reason |
|---|---|---|---|
| F1 | CMDB has 2,900 agent-discovered records; network scan found 1,327 more | **CHAIN** | Establishes the unmanaged estate — the attacker's blind spot |
| F2 | The 1,327 extra devices: no CMDB, no patching, no scanning, no compliance figure | **CHAIN** | Confirms these devices are invisible to all security controls |
| F3 | Compliance figures since 2024 computed as % of CMDB only; always >97% | context | Explains why leadership had false confidence — not a chain step |
| F4 | 318 of 340 printers use vendor default password on web admin interface | **CHAIN** | The entry point — trivially accessible from any network host |
| F5 | Printer web admin exposes stored service account credentials (svc-printscan + svc-printldap) | **CHAIN** | Credential harvest from printer — the pivot mechanism |
| F6 | svc-printldap is Domain Users + Print-Admins (no extra rights beyond Domain Users) | context | Clarifies that svc-printldap has no useful elevated privileges |
| F7 | svc-printscan has write on Scans AND Rundowns share (granted 2021 for wire copy) | **CHAIN** | svc-printscan is the high-value credential — access to newsroom content |
| F8 | Rundowns share holds newsroom rundowns and scripts; readable by newsroom group, writable by svc-printscan | **CHAIN** | Defines what the attacker can access and steal |
| F9 | Forum post contains internal Kaveri rundown matched to a Rundowns share file | **CHAIN** | Proves attacker accessed and exfiltrated newsroom rundowns |
| F10 | SNMP v2c across all switches, routers, UPS, PDUs — read+write community strings, both set in 2018, identical across all sites | **CHAIN** | The weapon: write string allows config changes on any network device |
| F11 | SNMP v2c transmits community string in plaintext; write string = full config control of any device | **CHAIN** | Confirms no authentication barrier for network device manipulation |
| F12 | Switch config backup shows port VLAN assignment change on Chennai gallery dist. switch (1 May → 9 May) | **CHAIN** | Confirms the network change that caused the outage |
| F13 | Change in F12 altered VLAN assignment on 8 playout server ports; servers still ran; automation log shows no schedule change | **CHAIN** | VLAN isolation caused channels to go black without touching the servers |
| F14 | Playout automation log shows outputs commanded normally throughout outage | **CHAIN** | Confirms the disruption was network-layer, not application-layer |
| F15 | Playout servers carry endpoint agent; no alert raised on any playout server | context | Confirms attacker didn't touch the servers themselves |
| F16 | 26 building management controllers accept unauthenticated commands; on corporate network | **CHAIN** | The building automation attack vector |
| F17 | Chennai gallery air handling controller shows setpoint change + disable command at 20:02 on 9 May | **CHAIN** | Building automation attack executed — caused thermal risk in rack room |
| F18 | BMC fleet on dedicated management network, reachable from corporate; firmware not updated since 2018–2022 | **CHAIN** | BMC as a potential persistence/deeper access path (F20 confirms activity) |
| F19 | BMCs allow remote console and virtual media — equivalent to physical server access | **CHAIN** | Confirms blast radius if BMCs were fully exploited |
| F20 | 11 BMCs show virtual media mount events (oldest retained entries, undatable) | **CHAIN** | Evidence of BMC usage — attacker likely established persistence or staging |
| F21 | Corporate-to-management-network firewall never configured to log | **CHAIN** | Evidence gap: no record of BMC access timing |
| F22 | Media asset management audit: 41,000 asset reads by svc-printscan (2 Feb – 8 May); svc-printscan has no legitimate MAM role | **CHAIN** | Attacker used printer credential to exfiltrate content library — 3 months of access |
| F23 | MAM authenticates against directory and authorises any Domain Users member to read the library | **CHAIN** | Explains why svc-printscan (Domain Users) had full read access to content library |
| F24 | Monthly vuln scan covers only CMDB (2,900 hosts); April 2027 report: 99.1% scanned, no critical findings | context | Confirms scan coverage was meaningless for this attack path |
| F25 | Annual pentest (Nov 2026) excluded printers, network devices, physical security, building services | **CHAIN** | Confirms the entire attack surface was explicitly out of pentest scope |
| F26 | Managed print contract has no security requirement, no default cred change obligation, no audit right | context | Contractual failure explaining why printers stayed at default creds |
| F27 | Monitoring platform holds the SNMP write community string; platform is on a patched Windows server with agent | context | The string was stored somewhere — not the exploit path itself |
| F28 | Monitoring platform recorded the 8 playout port transitions at 19:57 on 9 May; alert sent to shared mailbox (business hours only) | **CHAIN** | Alert existed but was unseen outside business hours — missed detection |
| F29 | 410,000 refused internet edge attempts from 13,000 addresses (1–6 Mar 2027); all refused | **DECOY** | Routine internet background noise; all refused; unrelated to attack |
| F30 | svc-printldap authenticated 6,100 times (Feb–May 2027) vs baseline ~400/month = ~15× normal | **CHAIN** | Anomalous directory auth confirms active attacker use of printer credential |
| F31 | No human Kaveri account compromised; MFA enforced on remote access and privileged accounts | **DECOY** | Confirms attack used service accounts only, not human accounts — NOT a red herring finding but confirms the non-human path |
| F32 | Security team aware of discovery gap since 2025; proposal not funded because CMDB compliance was >97% | context | Explains organisational failure — not a chain step |

### Confirmed Decoys (exclude from kill chain)

| Finding | Why excluded |
|---|---|
| **F29** | Routine internet background noise; all refused at edge; unrelated to attack vector |
| **F31** | Confirms no human account was used — reinforces the service account path, not a decoy but validates the chain |

---

## THE KILL CHAIN — 6 Steps

### Phase 1 — Initial Access via Unmanaged Printer

**Step 1 — Printer Default Credentials → Service Account Harvest** `(F1 → F2 → F4 → F5)`

1,327 network devices are invisible to every Kaveri security control (F1, F2). Among these: 318 of
340 printers use vendor default passwords on their web admin interface (F4). The web admin interface
exposes stored service account credentials for `svc-printscan` and `svc-printldap` (F5) — retrievable
by any user who can reach the interface. No authentication change is required; default password is
the only barrier.

---

### Phase 2 — Data Exfiltration (2 February – 8 May 2027)

**Step 2 — svc-printscan → Newsroom Rundowns + Media Asset Library** `(F7 → F8 → F9 → F22 → F23)`

`svc-printscan` has write access to the Rundowns share (granted in 2021, F7) which holds the
newsroom's scripts and rundowns (F8). The media asset management system authorises any Domain Users
member to read the full content library (F23), and `svc-printscan` is Domain Users.

Between 2 February and 8 May the attacker uses `svc-printscan` to make 41,000 asset reads from
the MAM content library (F22) and accesses the Rundowns share — the forum post on 9 May contains
an internal rundown file directly matched from the share (F9). Three months of continuous content
exfiltration.

---

### Phase 3 — Network Disruption via SNMP Write

**Step 3 — SNMP Write Community String → VLAN Reconfiguration → Broadcast Blackout** `(F10 → F11 → F12 → F13 → F14)`

All network switches, routers and power devices are monitored via SNMP v2c (F10). The protocol
transmits the community string in plaintext (F11) — the attacker can observe it by sniffing, or
by reading it from the monitoring platform via the earlier access path. Holding the write string
allows configuration changes on any device.

Between 1 and 9 May, the attacker modifies the VLAN assignment of 8 switch ports on the Chennai
gallery distribution switch serving the four playout server pairs (F12, F13). At 19:58 on 9 May
the channels go to black. Playout servers remain powered and running; the automation system
continues to command normally (F14) — the disruption is purely network isolation via VLAN
reconfiguration. The monitoring platform detects the port transitions at 19:57 but the alert
reaches an unmonitored shared mailbox (F28).

---

### Phase 4 — Building Automation Attack

**Step 4 — Unauthenticated Building Management Commands → Thermal Incident** `(F16 → F17)`

The 26 building management controllers for studio air handling accept commands over a building
automation protocol with no authentication, and sit on the corporate network (F16). At 20:02 on
9 May — 4 minutes into the outage — the attacker sends a setpoint change and a disable command to
the Chennai gallery air handling unit (F17). The rack room temperature rises to 41°C before
portable cooling is deployed.

---

### Phase 5 — Persistence via Baseboard Management Controllers

**Step 5 — BMC Virtual Media Mounts → Potential Deep Persistence** `(F18 → F19 → F20 → F21)`

410 server baseboard management controllers sit on a dedicated management network reachable from
corporate, running firmware from 2018–2022 (F18). BMCs permit remote console and virtual media —
equivalent to physical server access (F19). Eleven BMCs show virtual media mount events (oldest
retained entries, undatable due to 200-entry overwrite) (F20). The corporate-to-management-network
firewall has never logged (F21). These events likely represent persistence staging but cannot be
precisely timed.

---

## Kill Chain Summary (Portal Entry Format)

```
Step 1 — INITIAL ACCESS: PRINTER DEFAULT CREDENTIALS → SERVICE ACCOUNT HARVEST (F4 → F5)
318 of 340 printers use vendor default password. Web admin exposes stored svc-printscan and
svc-printldap credentials — retrievable by any network host. All 340 printers are unmanaged
(F1, F2): no CMDB, no patching, no scanning. Attacker accesses printer, extracts both credentials.

Step 2 — DATA EXFILTRATION: NEWSROOM RUNDOWNS + MEDIA ASSET LIBRARY (2 Feb – 8 May) (F7 → F8 → F22 → F23 → F9)
svc-printscan has write on Rundowns share (newsroom scripts). MAM authorises any Domain Users
member to read full content library (F23). Attacker makes 41,000 asset reads in MAM (F22) and
steals rundowns — exfiltrated rundown posted publicly on 9 May (F9). Three months of access.

Step 3 — NETWORK DISRUPTION: SNMP WRITE → VLAN RECONFIGURATION → BROADCAST BLACKOUT (9 May) (F10 → F11 → F12 → F13)
All network devices use SNMP v2c with single write community string across all three sites (F10).
String transmitted in plaintext (F11). Attacker modifies VLAN assignment on 8 playout switch ports
on Chennai gallery distribution switch (F12). At 19:58 all four channels go to black. Servers stay
running; automation system commands normally — disruption is network isolation only (F13, F14).

Step 4 — BUILDING AUTOMATION: UNAUTHENTICATED COMMANDS → THERMAL INCIDENT (20:02, 9 May) (F16 → F17)
Building management controllers accept unauthenticated commands on corporate network (F16).
At 20:02 attacker disables Chennai gallery air handling — rack room reaches 41°C (F17).

Step 5 — PERSISTENCE: BMC VIRTUAL MEDIA MOUNTS (UNDATED) (F18 → F19 → F20)
BMC fleet reachable from corporate, firmware from 2018–2022 (F18). 11 BMCs show virtual media
mount events — undatable due to log overwrite (F20). Firewall never logged (F21). Likely staging
or persistence established during the January–May access window.
```

---

## Evidence Gaps

| Gap | Reason |
|---|---|
| SNMP community string acquisition method | No logging on management-to-corporate firewall; no SNMP capture |
| BMC activity timing | 200-entry log overwritten; no firewall log (F21) |
| Full scope of content exfiltration | MAM audit has no alerting; printer logs record no access events |
| Access vector to printing network | Printers on corporate network but no firewall logs between segments |
