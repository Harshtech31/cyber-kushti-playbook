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

### Phase 1 — Initial Access via Unmanaged Printer

**Step 1 — Initial Credential Harvesting via Default Printer Web Interfaces** `(F4 → F5 → F6 → F7)`

The attacker accessed one or more of the 318 (out of 340) multifunction printers operating with default
vendor web administration passwords (F4). As documented by the vendor, the administrative interface exposes
stored service credentials in plaintext (F5). The attacker extracted two Active Directory accounts:
`KAVERI\svc-printldap` (used for directory address book queries) and `KAVERI\svc-printscan` (used for
scan-to-folder file share writes) (F5, F6, F7).

---

### Phase 2 — Reconnaissance & Content Exfiltration

**Step 2 — Reconnaissance, Content Library Access, and Rundown Exfiltration** `(F7 → F8 → F9 → F22 → F23 → F30)`

Between 2 February and 8 May 2027, the attacker used `svc-printldap` to perform abnormal directory
reconnaissance, generating 6,100 authentications (a 15x spike over the ~400/month baseline) (F30).
Leveraging `svc-printscan`'s standard Domain Users membership, the attacker performed 41,000 unauthorized
asset read operations in the Media Asset Management (MAM) system, where the account held no legitimate
business role (F22, F23). Furthermore, because `svc-printscan` held write access to the Rundowns file share
(granted in 2021), the attacker accessed newsroom scripts, successfully exfiltrating an internal bulletin
rundown that was subsequently leaked to a public forum on 9 May (F7, F8, F9).

---

### Phase 3 — Network Disruption via SNMPv2c

**Step 3 — Denial of Service via Network VLAN Reconfiguration** `(F10 → F11 → F12 → F13 → F14 → F15 → F28)`

The attacker used the global, plaintext SNMPv2c write community string—which had been set in 2018 and shared
identically across all network switches, routers, and PDUs across all three sites (F10, F11)—to modify the
Chennai gallery distribution switch (F12). At 19:57 on 9 May, the switch changed the VLAN assignments for
eight ports serving all four active/standby playout server pairs (F12, F13, F28). This immediately severed
playout network connectivity at 19:58, causing all four regional channels to drop to black simultaneously
while the servers and automation remained running normally (F13, F14, F15).

---

### Phase 4 — Building Automation Attack

**Step 4 — Studio Infrastructure Disruption via Unauthenticated Building Automation** `(F16 → F17, Section 3)`

At 20:02 on 9 May (four minutes into the broadcast blackout), the attacker sent network commands across
the corporate network to the Chennai gallery air handling unit controller (F16, F17). Because the 26
building management controllers accept commands over an unauthenticated building automation protocol (F16),
the attacker successfully applied a setpoint change and a disable command (F17). This shut down the studio
air handling, driving rack room ambient temperatures up to 41°C before portable cooling was manually
deployed (F17, Section 3).

---

## Kill Chain Summary (Portal Entry Format)

```
Step 1 — INITIAL CREDENTIAL HARVESTING VIA DEFAULT PRINTER WEB INTERFACES (F4 → F5 → F6 → F7)
Attacker accesses unmanaged printers with vendor default passwords (F4). Extracts stored plaintext
credentials for KAVERI\svc-printldap (directory queries) and KAVERI\svc-printscan (file share writes) (F5).

Step 2 — RECONNAISSANCE, CONTENT LIBRARY ACCESS, AND RUNDOWN EXFILTRATION (F7 → F8 → F9 → F22 → F23 → F30)
svc-printldap abused for directory recon (6,100 auths, 15x spike) (F30). svc-printscan used for 41,000
unauthorized MAM asset reads (F22, F23) and exfiltrating newsroom scripts from Rundowns share (F7, F8),
leaked to public forum on 9 May (F9).

Step 3 — DENIAL OF SERVICE VIA NETWORK VLAN RECONFIGURATION (F10 → F11 → F12 → F13 → F14 → F15 → F28)
Attacker uses global plaintext SNMPv2c write community string (F10, F11) to alter VLAN assignments on 8
playout switch ports on Chennai gallery distribution switch at 19:57 (F12, F13, F28). Causes simultaneous
broadcast blackout at 19:58 while playout servers and automation remain running normally (F13, F14, F15).

Step 4 — STUDIO INFRASTRUCTURE DISRUPTION VIA UNAUTHENTICATED BUILDING AUTOMATION (F16 → F17, Section 3)
At 20:02 on 9 May, attacker sends unauthenticated commands to Chennai gallery air handling unit controller
(F16). Applies setpoint change and disable command (F17), driving rack room temperature to 41°C (Section 3).
```

---

## Evidence Gaps

| Gap | Reason |
|---|---|
| SNMP community string acquisition method | No logging on management-to-corporate firewall; no SNMP capture |
| BMC activity timing | 200-entry log overwritten; no firewall log (F21) |
| Full scope of content exfiltration | MAM audit has no alerting; printer logs record no access events |
| Access vector to printing network | Printers on corporate network but no firewall logs between segments |
