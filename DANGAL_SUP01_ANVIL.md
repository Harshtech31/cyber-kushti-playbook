# DANGAL — SUP-01: Anvil Systems
> **Scenario type:** Supply chain  
> **Deadline:** 24 Sep 2026, 11:00 PM IST  
> **Status:** Kill chain updated with exact portal findings (6 steps)

---

## Quick Reference — What Happened

Anvil Systems publishes an infrastructure observability agent that runs with **root privilege** on critical enterprise servers (payment hosts, domain controllers, databases).

An attacker achieved a supply-chain compromise not through source code or Git repository tampering, but through a **build-pipeline interception on BUILD-01**:
1. Exploited an unpatched, publicly disclosed RCE plugin vulnerability on the internet-facing CI server (`BUILD-01`).
2. Identified that the release signing step blindly signs whatever files exist in the staging directory at that moment, without checking compiler output provenance.
3. Swapped pre-compiled malicious agent binaries into the staging directory post-compilation/testing, extending build duration by 15–18 minutes across 3 builds (v4.11.2, v4.12.1, v4.13.0).
4. The CI job automatically signed the backdoored binaries with Anvil's legitimate release key.
5. Published to the distribution CDN; customer agents verified the valid signature and auto-updated every 4 hours.
6. The agent executed with root privilege on customer infrastructure, beaconing outbound encrypted telemetry every 47 hours to a C2 domain registered on 18 Feb 2027.
7. Due to non-reproducible builds and absent published hash records, Anvil cannot identify which versions are affected.

---

## Finding Classification — All 32 Findings

| # | One-line summary | CHAIN / DECOY | Reason |
|---|---|---|---|
| **F1** | BUILD-01 plugin has unauthenticated RCE disclosed Nov 2026 with fix available | **CHAIN** | Initial access vulnerability on CI/CD server |
| **F2** | BUILD-01 web interface reachable from internet; no patching schedule | **CHAIN** | Internet exposure enabling initial exploit |
| **F3** | BUILD-01 OS logs retain 14 days locally, rotate by size, not forwarded | **CHAIN** | Forensics/evidence gap — host logs rotated out |
| **F4** | BUILD-01 is a server, not covered by endpoint detection | **CHAIN** | Lack of EDR telemetry on the build server |
| **F5** | CI job history: 214 release executions between Jan 2026 and Jun 2027 | **CHAIN** | Baseline for identifying anomalous builds |
| **F6** | 3 jobs had durations of 52, 49, 54 min (vs normal 31–38 min) on 2 Mar, 11 Apr, 23 May | **CHAIN** | Proves build tampering window for 3 releases |
| **F7** | Console output of the 3 jobs identical in structure, no error/anomaly | **CHAIN** | Explains why automated pipeline logs showed no failure |
| **F8** | Release job: checkout tag, compile for 6 platforms, test, write to staging dir, sign, publish | **CHAIN** | The build pipeline sequence |
| **F9** | Signing step reads whatever files are in staging dir; no verification against compile step | **CHAIN** | Critical architectural flaw enabling binary swap |
| **F10** | Release key in software keystore on BUILD-01, unlocked at job start by stored passphrase | **CHAIN** | Signing capability automated on the compromised host |
| **F11** | Agent verifies signature against embedded public key; signature on affected hosts is valid | **CHAIN** | Trojanized binaries carry authentic Anvil signature |
| **F12** | Manifest lists filenames, versions, hashes over HTTPS; manifest not separately signed | **CHAIN** | Delivery mechanism |
| **F13** | Builds not reproducible (embeds timestamp and host identifier) | **CHAIN** | Forensic gap preventing comparison with source rebuild |
| **F14** | Anvil keeps no record of published artifact hashes | **CHAIN** | Forensic gap preventing post-publication verification |
| **F15** | Code hosting platform audit log retains 180 days | context | Audit trail for repository events |
| **F16** | Tag v4.11.2 created 2 Mar and moved 40 min later to a different commit | **DECOY** | Red herring: looked suspicious initially |
| **F17** | Tag move was to descendant commit pushed by Anvil engineer, approved by 2 reviewers | **DECOY** | Legitimate developer activity |
| **F18** | PR titled "fix: handle empty config section on startup", 31 lines across 2 files | **DECOY** | Legitimate bugfix |
| **F19** | Source review confirmed no malicious code in repo / any commit | **DECOY** | Confirms supply chain compromise was NOT in source code |
| **F20** | Staff SSO log: no anomalous authentication; hardware keys enforced | **DECOY** | Confirms developer accounts were not compromised |
| **F21** | 400 customers running 61 distinct versions | context | Scale of customer deployment |
| **F22** | Agents check for updates every 4 hours | **CHAIN** | Automatic distribution mechanism |
| **F23** | Distribution server access log: downloads of every version | **CHAIN** | Delivery confirmed |
| **F24** | CDN log retains 30 days, no file hashes | context | Distribution telemetry |
| **F25** | Affected customers run versions 4.11.2 and 4.13.0 | **CHAIN** | Links customer infections to the anomalous builds |
| **F26** | Anomalous job durations (F6) match releases 4.11.2, 4.12.1, and 4.13.0 | **CHAIN** | Proves which three builds were poisoned |
| **F27** | Branch protection requires 2 approvals; commits not signed | context | Repo governance |
| **F28** | Pen test covered analysis platform only, excluded build infra | context | Governance failure |
| **F29** | Bug bounty excluded internal engineering infrastructure | context | Governance failure |
| **F30** | Security team knew BUILD-01 was unpatched; assumed internal-only | **CHAIN** | Governance failure enabling F2 exposure |
| **F31** | C2 domain registered 18 Feb 2027; contacted at 47-hour intervals | **CHAIN** | Attacker C2 infrastructure |
| **F32** | Anvil cannot tell customers which versions affected | **CHAIN** | Result of F13 and F14 |

---

## THE KILL CHAIN — 6 Steps (Matches UI)

### Step 1 — Initial Compromise of Internet-Exposed CI Server (BUILD-01)
- **Title:** Initial Access — Unauthenticated RCE on Exposed Build Server (BUILD-01)
- **Command / Tool:** HTTP exploit targeting unpatched automation product plugin
- **Details:** The release build server BUILD-01 had its web interface directly reachable from the internet to allow external contributor status reporting (F2, F30). The attacker exploited an unauthenticated remote code execution (RCE) vulnerability in an installed plugin that had been publicly disclosed in November 2026 but left unpatched (F1). Because BUILD-01 was exempted from endpoint detection (F4) and its local operating system logs rotated without central forwarding (F3), the attacker established unmonitored command execution on the host.

### Step 2 — Build Pipeline Reconnaissance & Identification of Signing Blind Spot
- **Title:** Pipeline Reconnaissance — Identification of Staging Directory Flaw
- **Command / Tool:** Local file inspection & CI job configuration review
- **Details:** Operating on BUILD-01, the attacker inspected the continuous integration job history and configuration (F5). The release pipeline checked out release tags, compiled for six architectures, ran tests, wrote outputs to a staging directory, invoked code signing, and published artifacts (F8). The attacker identified a critical flaw in the pipeline: the signing task simply signed whatever files existed in the staging directory at runtime without verifying their cryptographic hash or provenance against the compilation step (F9).

### Step 3 — Staging Directory Binary Interception on Target Releases
- **Title:** Build-Time Binary Swap in Staging Directory
- **Command / Tool:** Filesystem script replacing compiled binaries in staging directory
- **Details:** During release builds for versions 4.11.2, 4.12.1, and 4.13.0, the attacker allowed normal compilation and test suites to complete, then swapped in pre-compiled trojanized agent binaries directly into the staging directory before the signing step executed. This intervention extended the build duration by 15–18 minutes (52, 49, and 54 minutes vs normal 31–38 minutes) across the three dates: 2 March, 11 April, and 23 May 2027 (F6, F26). The standard console output logged no errors because the pipeline tasks completed successfully (F7). Source code in the repository remained completely untampered (F17, F18, F19).

### Step 4 — Automated Code Signing of Backdoored Binaries
- **Title:** Legitimate Cryptographic Code Signing of Trojanized Artifacts
- **Command / Tool:** Anvil Release Signing Job using local software keystore
- **Details:** Following the binary swap, the automated pipeline proceeded to the signing step, reading the modified files from the staging directory (F9). The job unlocked Anvil’s release key from the local software keystore on BUILD-01 using passphrases stored in the CI credential store (F10). The trojanized binaries were signed with Anvil's legitimate release key, embedding valid digital signatures that matched the public key hardcoded into the agent (F11).

### Step 5 — Signed Distribution via CDN to Enterprise Customer Base
- **Title:** Supply Chain Distribution via Legitimate Auto-Update Channel
- **Command / Tool:** HTTPS Distribution Server & CDN update manifest
- **Details:** The legitimately signed trojanized binaries and the updated manifest were published to Anvil's distribution server behind the CDN (F12). Enterprise customer agents polled the distribution server every 4 hours for updates (F22). Upon downloading the packages, customer agents verified Anvil's digital signature, found it valid, and executed the automated upgrade (F11, F23). Compromised versions (including 4.11.2 and 4.13.0) were deployed across high-value enterprise infrastructure (F25).

### Step 6 — Root-Level C2 Execution & Forensic Indefensibility
- **Title:** Persistent Root C2 Beacons & Remediation Paralysis
- **Command / Tool:** Outbound encrypted HTTPS beacons (47-hour interval)
- **Details:** The observability agent ran with root privileges on mission-critical servers, including domain controllers, payment processors, and database clusters across 400 enterprise clients (Section 1). The trojanized agent initiated outbound encrypted connections at 47-hour intervals to an external C2 domain registered on 18 February 2027 (F25, F31, Section 3). Because builds were non-reproducible due to embedded timestamps and host IDs (F13), and Anvil maintained no post-publication artifact hash registry (F14), the company was forensically incapable of determining which releases across its 61 active versions were compromised (F32).
