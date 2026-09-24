# ROUND 2 — THE DANGAL: KILL CHAIN MASTER INDEX
> **Team:** Null Theory · CK26-00638  
> **Portal:** https://hackathon.nsd.org.in  
> **Deadline:** 24 Sep 2026, **11:00 PM IST**  
> **Plan:** Start portal entry at **5:00 PM IST**

---

## ⚠️ Deadline

Submission window closes **24 Sep 2026, 11:00 PM IST**. Start entering at 5 PM.

---

## All 5 Scenarios

| ID | Name | Type | File | Steps | Decoys | Status |
|---|---|---|---|---|---|---|
| **WEB-01** | Northwind Goods | Web | [DANGAL_WEB01_NORTHWIND.md](DANGAL_WEB01_NORTHWIND.md) | 8 | F5, F6, F25, F26 | ❌ |
| **CLD-01** | Meridian Health Analytics | Cloud | [DANGAL_CLD01_MERIDIAN.md](DANGAL_CLD01_MERIDIAN.md) | 6 | F26, F27, F28 | ❌ |
| **OT-02** | Sundara Pharmaceuticals | OT | [DANGAL_OT02_SUNDARA.md](DANGAL_OT02_SUNDARA.md) | 5 | F23, F28, F29 | ❌ |
| **INF-02** | Kaveri Broadcast Network | Infrastructure | [DANGAL_INF02_KAVERI.md](DANGAL_INF02_KAVERI.md) | 5 | F29, F31 | ❌ |
| **SUP-01** | Anvil Systems | Supply chain | [DANGAL_SUP01_ANVIL.md](DANGAL_SUP01_ANVIL.md) | 6 | F27, F29 | ❌ |

---

## WEB-01: Northwind Goods (Web — 8 steps)
> 2.1M records · ₹1.91 crore store credit fraud · 4,118 orders shipped free

```
1. Staging recon → GraphQL introspection dumps 214-op schema          (F1→F2→F3)
2. Batch-alias brute-force account recovery on staging                 (F7→F8→F9)
3. Session cookie portability: staging session accepted by production  (F29→F28)
4. Mass assignment → account_type=internal_ops on production          (F12→F13)
5. IDOR order enumeration: 186,400 lookups → 2.14 GB to EU host       (F14→F15→F16)
6. Stored SQL injection via review → weekly report dumps 2.1M records (F17→F18)
7. Race condition + mass assignment → ₹1.91cr fraudulent store credit (F19→F20→F21)
8. Forged unsigned payment callbacks → 4,118 orders shipped free       (F22→F23→F24)
```
**Decoys:** F5+F6 (authorized pentest) · F25 (global injection blocked) · F26 (legitimate API token)

---

## CLD-01: Meridian Health Analytics (Cloud — 6 steps)
> DB snapshot exfiltrated · 14M patient episodes mass-decrypted

```
1. svc-etl-legacy key printed in CI job logs; logs readable by any org principal  (F1→F2→F3→F4)
2. Wildcard PassRole → assume deployment role → launch admin instance              (F6→F7→F5→F8)
3. Admin instance creates DB snapshot → shares to external account cross-region    (F9→F10→F11)
4. Read Terraform state → DB master password + 9 parameter store secrets           (F12→F13→F14)
5. Assume Ardent role (no ext-ID) → read object inventory (map 3.1M objects)      (F22→F24→F23→F25)
6. svc-etl-legacy + permissive KMS policy → 2.89M decrypt calls on clinical data  (F16→F17→F18→F20)
```
**Decoys:** F26+F27 (authorized pentest, after initial access) · F28 (root account noise)

---

## OT-02: Sundara Pharmaceuticals (OT — 5 steps)
> Trojanized firmware → falsified batch record → contaminated batch released

```
1. Thermaxis corporate compromise → vendor tunnel → plant access (4 sessions, 2–5 Nov)  (F4→F1→F2→F31)
2. Unauthenticated OPC UA → deploy unsigned trojanized firmware to autoclave 3            (F7→F8→F9→F10→F11)
3. Trojanized firmware reports false 41-min hold to historian (impossible in 48-min gap)  (F13→F14→F15→F16)
4. ebr-histlink (audit-exempt) writes falsified data → no modification entries created   (F20→F21)
5. QP reviews complete, consistent record → releases contaminated batch                   (F22)
```
**Decoys:** F23 (clean environmental monitoring) · F28 (corporate firewall noise) · F29 (clean corp auth)

---

## INF-02: Kaveri Broadcast Network (Infrastructure — 5 steps)
> 3 months content exfiltrated · broadcast blackout · thermal incident

```
1. 318 printers use default password → extract svc-printscan + svc-printldap credentials  (F4→F5)
2. svc-printscan → 41,000 MAM reads + newsroom rundown exfiltration (2 Feb – 8 May)       (F7→F22→F23→F9)
3. SNMP v2c write string → reconfigure 8 playout server switch ports → 4-channel blackout (F10→F11→F12→F13)
4. Unauthenticated building management commands → disable Chennai air handling (41°C)     (F16→F17)
5. BMC virtual media mounts on 11 servers → likely persistence staging                    (F18→F19→F20)
```
**Decoys:** F29 (internet background noise) · F31 (no human account — confirms service account path)

---

## SUP-01: Anvil Systems (Supply chain — 6 steps)
> DLL injected into SCADA build → 214 customers updated → payload at 198 sites → 3 sites physical harm

```
1. Spear phish → macro execution → encoded PowerShell C2 (EDR alert auto-suppressed)   (F1→F2→F3→F4)
2. Okafor's creds → lateral movement to build-srv-01 (no EDR on build server)          (F5→F6→F7)
3. SYSTEM scheduled tasks for persistence on build server                               (F8→F9)
4. Inject telemetry-helper.dll into v4.2.1 SCADA build (no binary integrity check)     (F10→F11→F12→F13)
5. Package signed with valid Anvil EV cert → push to update server → 214 auto-updates  (F14→F15)
6. 15 Mar payload: 198 sites write wrong process setpoints; 3 sites safety systems fail (F18→F19→F20)
```
**Decoys:** F27 (ASLR researcher disclosure) · F29 (SCA CVE findings, different issue)

---

## 5 PM Entry Checklist

**Before entering:**
- [ ] Login: https://hackathon.nsd.org.in → mharshith801@gmail.com
- [ ] Navigate to The Dangal
- [ ] Confirm all 5 scenarios show "No kill chains yet"

**Entry order (recommended — hardest → easiest to keep momentum):**
1. WEB-01 (most steps, most complex)
2. CLD-01 (cloud, 6 steps)
3. SUP-01 (supply chain, 6 steps)
4. INF-02 (infrastructure, 5 steps)
5. OT-02 (OT, 5 steps — save for last, very clean narrative)

**For each scenario:**
1. Click "Start your kill chain"
2. Read the UI (step-by-step builder vs free text — adapt format)
3. Use the "Portal Entry Format" block in each scenario file
4. DO NOT include the decoy findings in the chain
5. One kill chain per scenario

**Team split at 5 PM:**
| Member | Task |
|---|---|
| M1 (Lead) | Drive portal, type kill chain steps |
| M2 (Code) | Read scenario file aloud, cross-check findings cited |
| M3 (Dynamic) | Watch for decoys, call them out before M1 types |

**Hard stop:** 10:30 PM — all 5 submitted, review, lock.
