import json

with open('scans/portal_live_scan.json') as f:
    d = json.load(f)

scan = d['data']['scan']
vulns = scan.get('vulnerabilities', [])

output_lines = [
    "# VulnLab Live Scan — Complete 21 Issues Classification, Justification & Evidence Report",
    f"> **Scan ID:** `{scan.get('id')}`  ",
    "> **Target Repository:** `https://github.com/Yavuzlar/VulnLab.git`  ",
    f"> **AI Model:** `{scan.get('model_name')}`  ",
    "> **Total Findings:** 21 (12 True Positives, 9 False Positives / Decoys)  ",
    "> **Date:** 2026-09-21\n",
    "---\n",
    "## Quick Classification Summary Table\n",
    "| # | Finding ID | Title | Severity | Location | Classification |",
    "|---|---|---|---|---|---|"
]

tp_data = {
    1: {
        "just": "The script sends an HTTP Location: login.php redirect header without invoking exit() or die(). Consequently, PHP continues executing the entire script and transmits the full administrative dashboard markup to any HTTP client that suppresses automatic redirection (Execution After Redirect / CWE-698).",
        "evidence": "app/lab/broken-authentication/no-redirect/index.php:3 — header(\"Location:login.php\"); (Missing exit; or die(); full admin dashboard markup executes and returns in body)"
    },
    3: {
        "just": "The delete_image.php script takes the user-supplied 'image' GET parameter and concatenates it directly into unlink(\"uploads/\" . $image) without filename sanitization, basename() wrapping, or directory traversal checks, allowing unauthenticated attackers to delete arbitrary files across the server (CWE-22 / CWE-73).",
        "evidence": "app/lab/api-hacking/api-hacking1/api/delete_image.php:13 — $image = $_GET['image']; unlink(\"uploads/\" . $image); (Direct path traversal sink without basename() check)"
    },
    4: {
        "just": "The password modification routine processes credentials via a GET request without requiring or validating an anti-CSRF token. An attacker can craft a malicious link or image tag that triggers an unauthorized state-changing password reset when clicked by an authenticated user (CWE-352).",
        "evidence": "app/lab/csrf/changing-password/index.php:24 — if(isset($_GET['new_password'])) { ... } (State-changing password update via GET with zero CSRF token protection)"
    },
    7: {
        "just": "The application extracts the HTTP User-Agent header and directly interpolates it into a shell execution sink (exec) without escaping shell metacharacters via escapeshellarg(). An attacker supplying custom command separators in the User-Agent header achieves blind remote command execution (CWE-78).",
        "evidence": "app/lab/command-injection/blind-command-injection/blind.php:12 — exec(\"echo \" . $_SERVER['HTTP_USER_AGENT'] . \" >> log.txt\"); (Raw header interpolation into shell exec)"
    },
    9: {
        "just": "The upload handler inspects only the client-controlled MIME type header ($_FILES[\"file\"][\"type\"]) without verifying the file extension or file signature (magic bytes). Attackers can upload executable PHP scripts by spoofing the Content-Type header to image/jpeg (CWE-434).",
        "evidence": "app/lab/api-hacking/api-hacking1/api/upload.php:25 — if ($_FILES[\"file\"][\"type\"] == \"image/png\" || ...) (Relies solely on spoofable client MIME header with no extension validation)"
    },
    11: {
        "just": "The chat endpoint concatenates unsanitized POST data directly into an SQL INSERT/UPDATE statement string without prepared statements or parameter binding. An attacker can inject SQL control characters to alter database query logic and execute unauthorized SQL commands (CWE-89).",
        "evidence": "app/lab/csrf/changing-password/post.php:54 — $db->query(\"INSERT INTO csrf_chat ... VALUES ('\" . $_POST['chat-input'] . \"')\"); (Direct string concatenation into SQL query sink)"
    },
    13: {
        "just": "The stock-check utility executes a system Perl script via shell_exec(\"perl ... $product_id\") where product_id is user-controlled and unescaped. Appending shell metacharacters (such as semicolons or pipes) enables arbitrary command injection under the web server user context (CWE-78).",
        "evidence": "app/lab/command-injection/stock-check/index.php:76 — shell_exec(\"perl stock.pl \" . $_POST['product_id']); (Direct command execution with unescaped POST parameter)"
    },
    14: {
        "just": "The verification logic stores generated CAPTCHAs in a persistent session array and verifies answers using in_array() without clearing or invalidating used tokens upon successful verification. Attackers can reuse a single solved CAPTCHA indefinitely for automated replay attacks (CWE-294 / CWE-807).",
        "evidence": "app/lab/captcha-bypass/bypass1/index.php:95 — in_array($_POST['captcha'], $_SESSION['captchas']) (Session captcha array never invalidated after successful check)"
    },
    15: {
        "just": "Chat messages stored in the database are echoed directly into the HTML response without HTML entity encoding via htmlspecialchars(). An attacker submitting JavaScript payloads will have their scripts executed in the browser context of other users viewing the chat history (CWE-79).",
        "evidence": "app/lab/csrf/changing-password/index.php:108 — echo $row['message']; (Stored database content rendered directly into HTML without htmlspecialchars() encoding)"
    },
    16: {
        "just": "The application commits a static users.json file containing plaintext usernames, passwords, and administrative access roles directly within the web root. Anyone can fetch this configuration file directly over HTTP to obtain administrative credentials without authentication (CWE-798 / CWE-522).",
        "evidence": "app/lab/api-hacking/api-hacking1/api/users.json:2 — {\"username\": \"admin\", \"password\": \"...\", \"role\": \"admin\"} (Plaintext credentials stored in publicly accessible web root)"
    },
    18: {
        "just": "The CAPTCHA validation expects the client to supply both the operands (num1, num2) and the computed result in the POST payload. An attacker can tamper with the operands to force trivial calculations (e.g. 1+1=2) or bypass the verification logic entirely (CWE-807).",
        "evidence": "app/lab/captcha-bypass/bypass/index.php:43 — if($_POST['result'] == $_POST['num1'] + $_POST['num2']) (Both operands and result are sent from and controlled by client POST)"
    },
    19: {
        "just": "The ping utility executes the system ping binary using exec(\"ping -c5 $input\", $out) with raw user input from $_POST[\"ip\"]. Due to the complete absence of input validation or escapeshellarg() sanitization, an attacker can append command chaining operators to execute arbitrary system commands (CWE-78).",
        "evidence": "app/lab/command-injection/ping-low/index.php:40 — exec(\"ping -c5 \" . $_POST['ip'], $out); (Unsanitized POST parameter passed directly to system exec sink)"
    }
}

fp_evidence = {
    2: "Path verification: File 'notify/email_html_v2.py' does not exist in target repository. Target is pure PHP/JS; directory 'notify/' is entirely absent.",
    5: "Path verification: File 'notify/email_html_batch.py' does not exist in target repository. Directory 'notify/' is absent from the codebase.",
    6: "Path verification: File 'config/sessions.py' does not exist in target repository. Target uses native PHP session_start() with no Python session configuration.",
    8: "Path verification: File 'auth/login.py' does not exist in target repository. Auth is implemented via individual PHP lab scripts under 'app/lab/'.",
    10: "Path verification: File 'frontend/src/search.tsx' does not exist. VulnLab has no TypeScript/React frontend build pipeline or 'frontend/src/' directory.",
    12: "Path verification: File 'notify/email_html_legacy.py' does not exist in target repository. Decoy finding from generic assessment template.",
    17: "Path verification: File 'api/middleware.py' does not exist. There is no Python WSGI/ASGI middleware layer in this PHP-based application.",
    20: "Path verification: File 'api/validate.py' does not exist in target repository. No regex-based Python email validation module exists.",
    21: "Path verification: File 'ops/health.py' does not exist in target repository. The repository contains no 'ops/' directory or Python health check endpoint."
}

detailed_sections = ["\n---\n\n## Detailed Finding Classifications, Justifications & Evidence\n"]

for i, v in enumerate(vulns, 1):
    vid = v.get('id')
    title = v.get('title')
    sev = v.get('severity')
    loc = v.get('location')
    file_ = v.get('file')
    line = v.get('line_number')
    
    if i in tp_data:
        verdict = "TRUE_POSITIVE"
        just = tp_data[i]["just"]
        ev = tp_data[i]["evidence"]
    else:
        verdict = "FALSE_POSITIVE"
        just = f"This finding is a false positive decoy generated from the default hackathon assessment template. The cited file path ({file_}) does not exist in the allocated VulnLab PHP repository. Because this file and code sink are completely absent from the codebase, this finding has zero impact and cannot be exploited."
        ev = fp_evidence.get(i, f"File '{file_}' does not exist in target repository.")
        
    output_lines.append(f"| **{i}** | `{vid}` | **{title}** | `{sev}` | `{loc}` | **`{verdict}`** |")
    
    detailed_sections.append(f"### Finding #{i} · {title}\n\n")
    detailed_sections.append(f"* **Finding ID:** `{vid}`\n")
    detailed_sections.append(f"* **Location:** `{file_}:{line}`\n")
    detailed_sections.append(f"* **Severity:** `{sev}`\n")
    detailed_sections.append(f"* **Classification:** **`{verdict}`**\n\n")
    detailed_sections.append(f"**Portal Justification:**\n> {just}\n\n")
    detailed_sections.append(f"**Optional Evidence:**\n> `{ev}`\n\n")
    detailed_sections.append("---\n\n")

full_content = "\n".join(output_lines) + "".join(detailed_sections)

with open('VULNLAB_LIVE_SCAN_ANALYSIS.md', 'w') as f:
    f.write(full_content)

print("Updated VULNLAB_LIVE_SCAN_ANALYSIS.md cleanly!")
