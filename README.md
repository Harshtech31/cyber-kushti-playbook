# Cyber Kushti 2026 - Team Master Playbook Repository

> **National Cybersecurity & AI Hackathon (NIELIT / MeitY / ISAC / CERT-In)**  
> **Target:** 921 Teams $\to$ Top 50 Advance (Top 5.4% Cutoff)  
> **Round 1 Schedule (15 September 2026):**  
> - **14:00 (2:00 PM)**: Portal Access Released (Tracking & Schema Reconnaissance)  
> - **17:00 (5:00 PM)**: Target Git Repo Released & Official Work Kicks Off  
> - **22:30 (10:30 PM)**: Content Freeze  
> - **22:45 (10:45 PM)**: Portal Submission Dispatch (15-min Safety Buffer)  
> - **23:00 (11:00 PM)**: Hard Deadline  

---

## Quick Navigation & Playbook Sitemap

| Resource | Purpose | Target User / Phase |
| :--- | :--- | :--- |
| [ROUND_1_CHEAT_SHEET.md](ROUND_1_CHEAT_SHEET.md) | **Step-by-step battle timeline (Phases 0–6) & candidate triage flowchart** | **Primary Round 1 Operating Sheet** |
| [COMPETITION_DAY_CHECKLIST.md](COMPETITION_DAY_CHECKLIST.md) | **Clock-driven master checklist with exact timestamped milestones** | All Members (M1, M2, M3) |
| [AI_PROMPTING_PLAYBOOK.md](AI_PROMPTING_PLAYBOOK.md) | **5 Production AI Prompts (Hunter, Devil's Advocate, Dynamic PoC, Fixes)** | M1 & M2 (AI Code Auditing) |
| [TRUE_VS_FALSE_POSITIVE_GUIDE.md](TRUE_VS_FALSE_POSITIVE_GUIDE.md) | **Top 10 False Positive Archetypes & 3-Step Verification Method** | Human Verification Filter |
| [FINDING_REPORT_TEMPLATE.md](FINDING_REPORT_TEMPLATE.md) | **Template A (True Positive) & Template B (False Positive Justification)** | Portal Reporting |
| [COMMAND_CHEAT_SHEET.md](COMMAND_CHEAT_SHEET.md) | **Fast copy-paste CLI commands (Semgrep, CodeQL, Gitleaks, Docker, ripgrep)** | M2 & M3 Execution |
| [RESPONSIBILITY_MATRIX.md](RESPONSIBILITY_MATRIX.md) | **3-Member Role Cards (M1: Lead, M2: Code, M3: Dynamic Runtime)** | Coordination & Handoffs |
| [CYBER_KUSHTI_2026_TEAM_MASTER_PLAYBOOK.md](CYBER_KUSHTI_2026_TEAM_MASTER_PLAYBOOK.md) | **Comprehensive end-to-end operational manual and rule definitions** | Full Reference |
| [MASTER_VULNERABILITY_CHECKLIST.md](MASTER_VULNERABILITY_CHECKLIST.md) | **Coverage checklist for Auth, IDOR, Logic, Injection, SSRF, AI/LLM** | Coverage Audit |
| [TRAINING_ROADMAP.md](TRAINING_ROADMAP.md) | **Prep scenarios, drills, and lab training exercises** | Preparation |

---

## Environment Setup One-Liner

```bash
# Activate pre-installed security environment with all tools in PATH:
source ~/.security-tools/venv/bin/activate

# Verify tools:
which semgrep codeql osv-scanner gitleaks trivy bandit pip-audit docker
```

---

## Core Rule of Engagement
> **"Automation finds signal. Humans determine truth. Dynamic testing proves impact. Clear evidence wins the argument."**
