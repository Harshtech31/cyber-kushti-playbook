# DANGAL — CLD-01: Meridian Health Analytics
> **Scenario type:** Cloud  
> **Deadline:** 24 Sep 2026, 11:00 PM IST  
> **Status:** NOT submitted — enter at 5 PM

---

## Quick Reference — What Happened

A cloud-targeted attacker found a machine user access key printed in CI job logs, used it to
escalate to an admin-level instance role via a wildcard PassRole policy, shared a database
snapshot to an external account, and then mass-decrypted 14 million patient episode records
by exploiting an overly permissive KMS key policy. The attacker also abused a monitoring
vendor's role (no external ID condition) to read object inventory reports. A legitimate
authorized pentest and background internet noise are the two main decoys.

---

## Finding Classification — All 32 Findings

| # | One-line summary | CHAIN / DECOY | Reason |
|---|---|---|---|
| F1 | CI job `nightly-claims-etl` prints `svc-etl-legacy` access key in every run's log | **CHAIN** | Credential exposure — the attacker's entry point |
| F2 | CI job logs readable by any org principal, retained 400 days | **CHAIN** | Explains how attacker read the key from outside |
| F3 | `svc-etl-legacy` key never rotated since 2021; grants R/W on `meridian-clinical` + DB describe | **CHAIN** | Stolen key grants immediate data access |
| F4 | 214 control plane calls via `svc-etl-legacy` from outside Meridian IPs (2 Sep – 14 Nov) | **CHAIN** | Confirms attacker actively using stolen credentials |
| F5 | Deployment role launches instance with `MeridianPlatformAdmin` profile on 4 Sep 03:12 | **CHAIN** | Privilege escalation to admin-level instance role |
| F6 | Deployment role has `iam:PassRole` with wildcard resource + instance launch permission | **CHAIN** | The vulnerability that enables F5 |
| F7 | Deployment role assumed 1,840 times; 44 from outside Meridian IPs | **CHAIN** | Attacker assumes deployment role from outside |
| F8 | Instance ran 41 min, terminated by own profile; VPC flow logs don't cover 4 Sep | **CHAIN** | Admin instance used as pivot; evidence gap on network activity |
| F9 | Manual DB snapshot created 4 Sep 03:31; permissions modified to add external account | **CHAIN** | Database snapshot exfiltrated to attacker-controlled account |
| F10 | Snapshot copied to second region 03:44; copy permissions also modified to external account | **CHAIN** | Cross-region copy; cost and usage report confirms transfer charge |
| F11 | Snapshot sharing is control plane only — no network log, no flow log entry | **CHAIN** | Explains why exfil produced no network evidence |
| F12 | 31 reads of `meridian-tfstate` by `svc-etl-legacy` (6–9 Sep); nightly job never reads it | **CHAIN** | Attacker reads Terraform state for additional secrets |
| F13 | Terraform state contains DB master password and 9 parameter store entries in plaintext | **CHAIN** | Attacker obtains DB credentials and other secrets |
| F14 | DB accessible from prod VPC and analytics peered network; master password unchanged since 2022 | **CHAIN** | Attacker can connect to DB using master password from F13 |
| F15 | DB audit log retains 7 days — relevant period outside retention | context | Evidence gap; not a chain step |
| F16 | KMS key policy: decrypt granted to any org principal with correct encryption context KEY (value not checked) | **CHAIN** | Overly permissive key policy — any org principal can decrypt |
| F17 | 3,110,000 decrypt calls 12 Sep – 2 Nov; 2,890,000 by `svc-etl-legacy` | **CHAIN** | Mass decryption of clinical records using stolen key |
| F18 | Normal decrypt rate ~41,000/month; 2,890,000 in ~2 months = ~70× normal | **CHAIN** | Anomaly confirming mass exfiltration scale |
| F19 | Object storage data events not enabled (cost decision in 2023) | context | Evidence gap explaining why no object access logs exist |
| F20 | Inventory report: no objects created, deleted or modified beyond expected daily ingest | **CHAIN** | Confirms attacker used in-place decryption (not copy/move) — method proof |
| F21 | `meridian-clinical`: ~3.1M objects, ~14M patient episodes | context | Scope of data at risk |
| F22 | Ardent role trust policy: no external ID condition, no source address condition | **CHAIN** | Confused deputy vulnerability — any holder of Ardent's account ID can assume the role |
| F23 | Ardent role assumed 890 times; 402 by Ardent; 488 from unknown addresses | **CHAIN** | Attacker abusing Ardent role 488 times |
| F24 | Ardent's account ID is in public product documentation | **CHAIN** | Explains how attacker found the account ID to use in AssumeRole |
| F25 | Ardent role grants: metrics read + inventory reports for `meridian-clinical` + DB describe | **CHAIN** | Attacker uses Ardent role to read inventory → learns object structure before decrypting |
| F26 | Pentest 15–19 Sep found wildcard PassRole (severity High); accepted, Q1 2027 remediation | **DECOY** | Authorized pentest — declared source addresses, scheduled; happened *after* initial access |
| F27 | 4,900 pentest calls from declared source addresses (15–19 Sep) | **DECOY** | Confirms F26 is authorized activity |
| F28 | 112,000 failed root sign-in attempts from 8,400 addresses, all failed | **DECOY** | Global internet campaign; root has hardware 2FA; cloud provider confirms mass campaign |
| F29 | 16 long-lived keys; 9 never rotated; 4 unidentified; quarterly review never covers machine users | context | Hygiene weakness explaining the problem but not a direct chain step |
| F30 | Controls report tested encryption by checking key exists, not examining key policy | context | Explains why overly permissive KMS policy was never caught in audit |
| F31 | Container platform task role has decrypt + read on `meridian-clinical`; job defs updatable by anyone with deployment role | context | Alternative exfil path that could have been used but is secondary to main chain |
| F32 | Cost and usage report reviewed only by finance monthly | context | Explains why cross-region transfer charge (F10) wasn't noticed sooner |

### Confirmed Decoys (exclude from kill chain)

| Finding | Why excluded |
|---|---|
| **F26** | Authorized pentest with declared sources — happened after initial access (2 Sep); PassRole was exploited before the pentest started (15 Sep) |
| **F27** | Confirms F26 is authorized pentest activity |
| **F28** | Global root account brute force; all failed; hardware 2FA; cloud provider mass campaign advisory |

---

## THE KILL CHAIN — 6 Steps

### Phase 1 — Credential Theft

**Step 1 — Access Key from CI Job Log** `(F1 → F2 → F3 → F4)`

The `nightly-claims-etl` CI job prints its full environment at the start of every run (F1).
Its logs have been readable by any org principal for 400 days (F2). The environment includes the
access key ID and secret for `svc-etl-legacy` — a machine user created in 2021 and never rotated
(F3) with read/write on `meridian-clinical` and DB describe access.

Attacker reads the CI log, extracts the key, and begins 214 control plane API calls from outside
any Meridian IP range between 2 September and 14 November (F4).

---

### Phase 2 — Privilege Escalation

**Step 2 — Wildcard PassRole → Admin Instance Role** `(F6 → F7 → F5 → F8)`

The deployment role carries `iam:PassRole` with a wildcard resource element, plus permission to
launch instances (F6). Attacker assumes the deployment role from outside Meridian (F7 — 44
assumptions from external IPs) and uses it to launch an EC2 instance specifying the
`MeridianPlatformAdmin` instance profile (F5). The instance runs for 41 minutes, executes
privileged operations, then terminates itself using its own instance profile (F8). VPC flow logs
do not cover 4 September.

---

### Phase 3 — Database Snapshot Exfiltration

**Step 3 — Snapshot to External Account** `(F9 → F10 → F11)`

Using `MeridianPlatformAdmin` privileges, attacker creates a manual snapshot of the production
relational database at 03:31 on 4 September (F9). At 03:36, snapshot permissions are modified
to add an external account identifier (no Meridian account, no known vendor). At 03:44, the
snapshot is copied to a second region; at 03:51, the copy's permissions are also modified to the
same external account (F10).

Snapshot sharing is a control plane operation — no data crosses a network Meridian can observe,
no flow log entry exists (F11). The cost and usage report records the cross-region transfer
charge (from F10). Database snapshot contains the derived analytics tables.

---

### Phase 4 — Terraform State → More Credentials

**Step 4 — Read Terraform State for Secrets** `(F12 → F13 → F14)`

The `meridian-tfstate` bucket is readable by any org principal (bucket policy: read to any org
principal). The `nightly-claims-etl` job has never read it. Between 6 and 9 September, `svc-etl-legacy`
makes 31 reads on Terraform state objects (F12). Terraform state contains the initial master
password for the production database instance in plaintext, plus nine parameter store entries
(F13). The database has accepted the unchanged master password since 2022 and is peered to the
analytics environment (F14).

---

### Phase 5 — Inventory Recon via Confused Deputy

**Step 5 — Assume Ardent Role (No External ID) → Read Object Inventory** `(F22 → F24 → F23 → F25)`

The monitoring vendor Ardent Observability's role trust policy names Ardent's account ID as
principal but carries no external ID condition (F22). Ardent's account ID is in its public product
documentation (F24). Attacker calls `AssumeRole` impersonating Ardent's account — 488 unexplained
role assumptions over September–November (F23 — Ardent's own records account for only 402 of
890 total). The Ardent role grants read on the object storage inventory reports for
`meridian-clinical` (F25). Attacker reads daily manifests to map all 3.1 million objects before
decrypting.

---

### Phase 6 — Mass Data Exfiltration via In-Place Decryption

**Step 6 — Decrypt 14 Million Patient Records** `(F16 → F17 → F18 → F20)`

The KMS customer managed key policy grants decrypt to any org principal whose request carries the
encryption context key `meridian/clinical` — the value is not checked, only the presence of the
key (F16). `svc-etl-legacy` is an org principal. Normal decrypt rate is ~41,000 calls/month (F18).

Between 12 September and 2 November, `svc-etl-legacy` makes 2,890,000 decrypt calls (F17) — 70×
normal volume. Objects are read and decrypted in place: the inventory report shows no objects
created, deleted, or modified beyond expected daily ingest (F20), confirming attacker used
client-side decryption rather than copying files.

14 million patient episode records from 11 hospital groups exfiltrated.

---

## Kill Chain Summary (Portal Entry Format)

```
Step 1 — CREDENTIAL THEFT FROM CI JOB LOG
nightly-claims-etl prints svc-etl-legacy access key in every run's environment output (F1).
CI job logs readable by any org principal for 400 days (F2). Key never rotated since 2021 (F3).
Attacker reads log, extracts key, begins 214 control plane calls from outside Meridian IPs (F4).

Step 2 — WILDCARD PASSROLE → ADMIN INSTANCE (4 Sep)
Deployment role has iam:PassRole with wildcard resource + instance launch permission (F6).
Attacker assumes deployment role from external IPs (F7 — 44 external assumptions). Launches
instance with MeridianPlatformAdmin profile (F5). Instance runs 41 min then self-terminates (F8).
VPC flow logs don't cover this date.

Step 3 — DATABASE SNAPSHOT TO EXTERNAL ACCOUNT (4 Sep)
MeridianPlatformAdmin creates manual DB snapshot at 03:31; modifies permissions to external
account at 03:36 (F9). Copies snapshot cross-region at 03:44; modifies copy permissions to same
external account at 03:51 (F10). Snapshot sharing is control plane only — no network log (F11).

Step 4 — TERRAFORM STATE → DB MASTER PASSWORD (6–9 Sep)
tfstate bucket readable by any org principal. svc-etl-legacy makes 31 reads on tfstate (F12),
obtaining the DB master password and 9 parameter store secrets (F13). DB accepts master password
unchanged since 2022 (F14).

Step 5 — CONFUSED DEPUTY: ASSUME ARDENT ROLE → READ OBJECT INVENTORY (Sep–Nov)
Ardent role trust policy has no external ID condition (F22). Ardent's account ID is in public docs
(F24). Attacker assumes Ardent role 488 times (F23). Role grants read on meridian-clinical
inventory reports (F25) — attacker maps all 3.1M objects before decrypting.

Step 6 — MASS IN-PLACE DECRYPTION OF 14M PATIENT RECORDS (12 Sep – 2 Nov)
KMS key policy grants decrypt to any org principal with encryption context key meridian/clinical
(value not checked) (F16). svc-etl-legacy makes 2,890,000 decrypt calls — 70× normal rate (F17,
F18). No objects created, deleted or modified (F20) — in-place decryption used throughout.
14 million patient episodes from 11 hospital groups exfiltrated.
```

---

## Evidence Gaps (document for judges)

| Gap | Reason |
|---|---|
| What the admin instance actually did (F8) | VPC flow logs don't cover 4 September; no data event logging |
| Database query content (F14, F15) | DB audit log retains 7 days; statements not recorded |
| Object access patterns (F19) | Object storage data events never enabled |
| Attacker's egress path for decrypted data | No egress monitoring; no endpoint detection on cloud workloads |
