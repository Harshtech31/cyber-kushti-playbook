# VulnLab Live Scan — Complete 21 Issues Classification, Justification & Evidence Report
> **Scan ID:** `3e367dfc-e3c7-4a82-b39a-a0f062291bb0`  
> **Target Repository:** `https://github.com/Yavuzlar/VulnLab.git`  
> **AI Model:** `gemini-3-flash-preview`  
> **Total Findings:** 21 (12 True Positives, 9 False Positives / Decoys)  
> **Date:** 2026-09-21

---

## Quick Classification Summary Table

| # | Finding ID | Title | Severity | Location | Classification |
|---|---|---|---|---|---|
| **1** | `3398f2af-2ec7-4b55-af6d-13d11a1e407d` | **Information Disclosure via Execution after Redirect** | `MEDIUM` | `app/lab/broken-authentication/no-redirect/index.php:3` | **`TRUE_POSITIVE`** |
| **2** | `1a7d5408-18ec-4885-8e36-514425c4afc6` | **XSS in notification preview (v2)** | `MEDIUM` | `notify/email_html_v2.py:37` | **`FALSE_POSITIVE`** |
| **3** | `3a2eef62-3eda-46a8-804e-445ae6d57ef1` | **Unrestricted File Deletion via Path Traversal** | `HIGH` | `app/lab/api-hacking/api-hacking1/api/delete_image.php:13` | **`TRUE_POSITIVE`** |
| **4** | `de7a064c-15c7-4e35-bd11-5ce9af4d89b9` | **Missing CSRF Protection on Password Change** | `HIGH` | `app/lab/csrf/changing-password/index.php:24` | **`TRUE_POSITIVE`** |
| **5** | `84699aaf-0dfa-4d64-83a8-137d11f06a94` | **XSS in notification preview (batch)** | `MEDIUM` | `notify/email_html_batch.py:39` | **`FALSE_POSITIVE`** |
| **6** | `7fbe739c-9e15-4d36-9191-3e6b99e6bbba` | **Session cookie without HttpOnly** | `LOW` | `config/sessions.py:6` | **`FALSE_POSITIVE`** |
| **7** | `0dacfb90-d7b0-4b0f-923b-5280eaacc99c` | **Blind Command Injection via User-Agent Header** | `CRITICAL` | `app/lab/command-injection/blind-command-injection/blind.php:12` | **`TRUE_POSITIVE`** |
| **8** | `683e4c0b-9fa3-4de9-a2fb-fd71fd927c9b` | **No rate limit on login** | `MEDIUM` | `auth/login.py:50` | **`FALSE_POSITIVE`** |
| **9** | `fef4233d-edc3-4ab2-9642-9f0a5e33725d` | **Insecure File Upload via MIME-Type Spoofing** | `HIGH` | `app/lab/api-hacking/api-hacking1/api/upload.php:25` | **`TRUE_POSITIVE`** |
| **10** | `1f129f5a-3dd6-4298-ae5f-f69e582b42e0` | **DOM XSS in search page** | `HIGH` | `frontend/src/search.tsx:41` | **`FALSE_POSITIVE`** |
| **11** | `5ebbbe4b-c569-4f5e-9957-440e1618a404` | **SQL Injection in Chat Message Storage** | `HIGH` | `app/lab/csrf/changing-password/post.php:54` | **`TRUE_POSITIVE`** |
| **12** | `c0bcd6f9-86fa-4ff0-8b86-7281842bf1d5` | **XSS in notification preview (legacy)** | `MEDIUM` | `notify/email_html_legacy.py:36` | **`FALSE_POSITIVE`** |
| **13** | `62978cf9-31cf-4f45-8592-cc079033a4d2` | **OS Command Injection via Perl Script Wrapper** | `CRITICAL` | `app/lab/command-injection/stock-check/index.php:76` | **`TRUE_POSITIVE`** |
| **14** | `475222ff-9b83-4943-9fd2-70b991b06b62` | **CAPTCHA Replay Vulnerability** | `MEDIUM` | `app/lab/captcha-bypass/bypass1/index.php:95` | **`TRUE_POSITIVE`** |
| **15** | `a60006d6-3c52-4399-ad2b-ba8efde63307` | **Stored XSS in Chat Functionality** | `HIGH` | `app/lab/csrf/changing-password/index.php:108` | **`TRUE_POSITIVE`** |
| **16** | `621e3530-13b4-4d14-a364-319959515316` | **Hardcoded Credentials in JSON Configuration** | `MEDIUM` | `app/lab/api-hacking/api-hacking1/api/users.json:2` | **`TRUE_POSITIVE`** |
| **17** | `28610450-bc05-4170-be88-2c9d26007cae` | **Stack traces returned to clients** | `LOW` | `api/middleware.py:27` | **`FALSE_POSITIVE`** |
| **18** | `a1d4d23b-a577-4bdf-865a-81ea9d657634` | **CAPTCHA Bypass via Client-Controlled Parameters** | `MEDIUM` | `app/lab/captcha-bypass/bypass/index.php:43` | **`TRUE_POSITIVE`** |
| **19** | `576a4228-d955-4fb0-b025-6a22a231319a` | **OS Command Injection in Ping Utility** | `CRITICAL` | `app/lab/command-injection/ping-low/index.php:44` | **`TRUE_POSITIVE`** |
| **20** | `96a00caf-5ecd-44b1-95f6-3ee015e7ee2c` | **ReDoS in email validator** | `LOW` | `api/validate.py:17` | **`FALSE_POSITIVE`** |
| **21** | `0bc96159-3e91-4559-bf7d-608dea348c77` | **Missing CSRF token on health check** | `LOW` | `ops/health.py:8` | **`FALSE_POSITIVE`** |
---

## Detailed Finding Classifications, Justifications & Evidence
### Finding #1 · Information Disclosure via Execution after Redirect

* **Finding ID:** `3398f2af-2ec7-4b55-af6d-13d11a1e407d`
* **Location:** `app/lab/broken-authentication/no-redirect/index.php:3`
* **Severity:** `MEDIUM`
* **Classification:** **`TRUE_POSITIVE`**

**Portal Justification:**
> The script sends an HTTP Location: login.php redirect header without invoking exit() or die(). Consequently, PHP continues executing the entire script and transmits the full administrative dashboard markup to any HTTP client that suppresses automatic redirection (Execution After Redirect / CWE-698).

**Optional Evidence:**
> `app/lab/broken-authentication/no-redirect/index.php:3 — header("Location:login.php"); (Missing exit; or die(); full admin dashboard markup executes and returns in body)`

---

### Finding #2 · XSS in notification preview (v2)

* **Finding ID:** `1a7d5408-18ec-4885-8e36-514425c4afc6`
* **Location:** `notify/email_html_v2.py:37`
* **Severity:** `MEDIUM`
* **Classification:** **`FALSE_POSITIVE`**

**Portal Justification:**
> This finding is a false positive decoy generated from the default hackathon assessment template. The cited file path (notify/email_html_v2.py) does not exist in the allocated VulnLab PHP repository. Because this file and code sink are completely absent from the codebase, this finding has zero impact and cannot be exploited.

**Optional Evidence:**
> `Path verification: File 'notify/email_html_v2.py' does not exist in target repository. Target is pure PHP/JS; directory 'notify/' is entirely absent.`

---

### Finding #3 · Unrestricted File Deletion via Path Traversal

* **Finding ID:** `3a2eef62-3eda-46a8-804e-445ae6d57ef1`
* **Location:** `app/lab/api-hacking/api-hacking1/api/delete_image.php:13`
* **Severity:** `HIGH`
* **Classification:** **`TRUE_POSITIVE`**

**Portal Justification:**
> The delete_image.php script takes the user-supplied 'image' GET parameter and concatenates it directly into unlink("uploads/" . $image) without filename sanitization, basename() wrapping, or directory traversal checks, allowing unauthenticated attackers to delete arbitrary files across the server (CWE-22 / CWE-73).

**Optional Evidence:**
> `app/lab/api-hacking/api-hacking1/api/delete_image.php:13 — $image = $_GET['image']; unlink("uploads/" . $image); (Direct path traversal sink without basename() check)`

---

### Finding #4 · Missing CSRF Protection on Password Change

* **Finding ID:** `de7a064c-15c7-4e35-bd11-5ce9af4d89b9`
* **Location:** `app/lab/csrf/changing-password/index.php:24`
* **Severity:** `HIGH`
* **Classification:** **`TRUE_POSITIVE`**

**Portal Justification:**
> The password modification routine processes credentials via a GET request without requiring or validating an anti-CSRF token. An attacker can craft a malicious link or image tag that triggers an unauthorized state-changing password reset when clicked by an authenticated user (CWE-352).

**Optional Evidence:**
> `app/lab/csrf/changing-password/index.php:24 — if(isset($_GET['new_password'])) { ... } (State-changing password update via GET with zero CSRF token protection)`

---

### Finding #5 · XSS in notification preview (batch)

* **Finding ID:** `84699aaf-0dfa-4d64-83a8-137d11f06a94`
* **Location:** `notify/email_html_batch.py:39`
* **Severity:** `MEDIUM`
* **Classification:** **`FALSE_POSITIVE`**

**Portal Justification:**
> This finding is a false positive decoy generated from the default hackathon assessment template. The cited file path (notify/email_html_batch.py) does not exist in the allocated VulnLab PHP repository. Because this file and code sink are completely absent from the codebase, this finding has zero impact and cannot be exploited.

**Optional Evidence:**
> `Path verification: File 'notify/email_html_batch.py' does not exist in target repository. Directory 'notify/' is absent from the codebase.`

---

### Finding #6 · Session cookie without HttpOnly

* **Finding ID:** `7fbe739c-9e15-4d36-9191-3e6b99e6bbba`
* **Location:** `config/sessions.py:6`
* **Severity:** `LOW`
* **Classification:** **`FALSE_POSITIVE`**

**Portal Justification:**
> This finding is a false positive decoy generated from the default hackathon assessment template. The cited file path (config/sessions.py) does not exist in the allocated VulnLab PHP repository. Because this file and code sink are completely absent from the codebase, this finding has zero impact and cannot be exploited.

**Optional Evidence:**
> `Path verification: File 'config/sessions.py' does not exist in target repository. Target uses native PHP session_start() with no Python session configuration.`

---

### Finding #7 · Blind Command Injection via User-Agent Header

* **Finding ID:** `0dacfb90-d7b0-4b0f-923b-5280eaacc99c`
* **Location:** `app/lab/command-injection/blind-command-injection/blind.php:12`
* **Severity:** `CRITICAL`
* **Classification:** **`TRUE_POSITIVE`**

**Portal Justification:**
> The application extracts the HTTP User-Agent header and directly interpolates it into a shell execution sink (exec) without escaping shell metacharacters via escapeshellarg(). An attacker supplying custom command separators in the User-Agent header achieves blind remote command execution (CWE-78).

**Optional Evidence:**
> `app/lab/command-injection/blind-command-injection/blind.php:12 — exec("echo " . $_SERVER['HTTP_USER_AGENT'] . " >> log.txt"); (Raw header interpolation into shell exec)`

---

### Finding #8 · No rate limit on login

* **Finding ID:** `683e4c0b-9fa3-4de9-a2fb-fd71fd927c9b`
* **Location:** `auth/login.py:50`
* **Severity:** `MEDIUM`
* **Classification:** **`FALSE_POSITIVE`**

**Portal Justification:**
> This finding is a false positive decoy generated from the default hackathon assessment template. The cited file path (auth/login.py) does not exist in the allocated VulnLab PHP repository. Because this file and code sink are completely absent from the codebase, this finding has zero impact and cannot be exploited.

**Optional Evidence:**
> `Path verification: File 'auth/login.py' does not exist in target repository. Auth is implemented via individual PHP lab scripts under 'app/lab/'.`

---

### Finding #9 · Insecure File Upload via MIME-Type Spoofing

* **Finding ID:** `fef4233d-edc3-4ab2-9642-9f0a5e33725d`
* **Location:** `app/lab/api-hacking/api-hacking1/api/upload.php:25`
* **Severity:** `HIGH`
* **Classification:** **`TRUE_POSITIVE`**

**Portal Justification:**
> The upload handler inspects only the client-controlled MIME type header ($_FILES["file"]["type"]) without verifying the file extension or file signature (magic bytes). Attackers can upload executable PHP scripts by spoofing the Content-Type header to image/jpeg (CWE-434).

**Optional Evidence:**
> `app/lab/api-hacking/api-hacking1/api/upload.php:25 — if ($_FILES["file"]["type"] == "image/png" || ...) (Relies solely on spoofable client MIME header with no extension validation)`

---

### Finding #10 · DOM XSS in search page

* **Finding ID:** `1f129f5a-3dd6-4298-ae5f-f69e582b42e0`
* **Location:** `frontend/src/search.tsx:41`
* **Severity:** `HIGH`
* **Classification:** **`FALSE_POSITIVE`**

**Portal Justification:**
> This finding is a false positive decoy generated from the default hackathon assessment template. The cited file path (frontend/src/search.tsx) does not exist in the allocated VulnLab PHP repository. Because this file and code sink are completely absent from the codebase, this finding has zero impact and cannot be exploited.

**Optional Evidence:**
> `Path verification: File 'frontend/src/search.tsx' does not exist. VulnLab has no TypeScript/React frontend build pipeline or 'frontend/src/' directory.`

---

### Finding #11 · SQL Injection in Chat Message Storage

* **Finding ID:** `5ebbbe4b-c569-4f5e-9957-440e1618a404`
* **Location:** `app/lab/csrf/changing-password/post.php:54`
* **Severity:** `HIGH`
* **Classification:** **`TRUE_POSITIVE`**

**Portal Justification:**
> The chat endpoint concatenates unsanitized POST data directly into an SQL INSERT/UPDATE statement string without prepared statements or parameter binding. An attacker can inject SQL control characters to alter database query logic and execute unauthorized SQL commands (CWE-89).

**Optional Evidence:**
> `app/lab/csrf/changing-password/post.php:54 — $db->query("INSERT INTO csrf_chat ... VALUES ('" . $_POST['chat-input'] . "')"); (Direct string concatenation into SQL query sink)`

---

### Finding #12 · XSS in notification preview (legacy)

* **Finding ID:** `c0bcd6f9-86fa-4ff0-8b86-7281842bf1d5`
* **Location:** `notify/email_html_legacy.py:36`
* **Severity:** `MEDIUM`
* **Classification:** **`FALSE_POSITIVE`**

**Portal Justification:**
> This finding is a false positive decoy generated from the default hackathon assessment template. The cited file path (notify/email_html_legacy.py) does not exist in the allocated VulnLab PHP repository. Because this file and code sink are completely absent from the codebase, this finding has zero impact and cannot be exploited.

**Optional Evidence:**
> `Path verification: File 'notify/email_html_legacy.py' does not exist in target repository. Decoy finding from generic assessment template.`

---

### Finding #13 · OS Command Injection via Perl Script Wrapper

* **Finding ID:** `62978cf9-31cf-4f45-8592-cc079033a4d2`
* **Location:** `app/lab/command-injection/stock-check/index.php:76`
* **Severity:** `CRITICAL`
* **Classification:** **`TRUE_POSITIVE`**

**Portal Justification:**
> The stock-check utility executes a system Perl script via shell_exec("perl ... $product_id") where product_id is user-controlled and unescaped. Appending shell metacharacters (such as semicolons or pipes) enables arbitrary command injection under the web server user context (CWE-78).

**Optional Evidence:**
> `app/lab/command-injection/stock-check/index.php:76 — shell_exec("perl stock.pl " . $_POST['product_id']); (Direct command execution with unescaped POST parameter)`

---

### Finding #14 · CAPTCHA Replay Vulnerability

* **Finding ID:** `475222ff-9b83-4943-9fd2-70b991b06b62`
* **Location:** `app/lab/captcha-bypass/bypass1/index.php:95`
* **Severity:** `MEDIUM`
* **Classification:** **`TRUE_POSITIVE`**

**Portal Justification:**
> The verification logic stores generated CAPTCHAs in a persistent session array and verifies answers using in_array() without clearing or invalidating used tokens upon successful verification. Attackers can reuse a single solved CAPTCHA indefinitely for automated replay attacks (CWE-294 / CWE-807).

**Optional Evidence:**
> `app/lab/captcha-bypass/bypass1/index.php:95 — in_array($_POST['captcha'], $_SESSION['captchas']) (Session captcha array never invalidated after successful check)`

---

### Finding #15 · Stored XSS in Chat Functionality

* **Finding ID:** `a60006d6-3c52-4399-ad2b-ba8efde63307`
* **Location:** `app/lab/csrf/changing-password/index.php:108`
* **Severity:** `HIGH`
* **Classification:** **`TRUE_POSITIVE`**

**Portal Justification:**
> Chat messages stored in the database are echoed directly into the HTML response without HTML entity encoding via htmlspecialchars(). An attacker submitting JavaScript payloads will have their scripts executed in the browser context of other users viewing the chat history (CWE-79).

**Optional Evidence:**
> `app/lab/csrf/changing-password/index.php:108 — echo $row['message']; (Stored database content rendered directly into HTML without htmlspecialchars() encoding)`

---

### Finding #16 · Hardcoded Credentials in JSON Configuration

* **Finding ID:** `621e3530-13b4-4d14-a364-319959515316`
* **Location:** `app/lab/api-hacking/api-hacking1/api/users.json:2`
* **Severity:** `MEDIUM`
* **Classification:** **`TRUE_POSITIVE`**

**Portal Justification:**
> The application commits a static users.json file containing plaintext usernames, passwords, and administrative access roles directly within the web root. Anyone can fetch this configuration file directly over HTTP to obtain administrative credentials without authentication (CWE-798 / CWE-522).

**Optional Evidence:**
> `app/lab/api-hacking/api-hacking1/api/users.json:2 — {"username": "admin", "password": "...", "role": "admin"} (Plaintext credentials stored in publicly accessible web root)`

---

### Finding #17 · Stack traces returned to clients

* **Finding ID:** `28610450-bc05-4170-be88-2c9d26007cae`
* **Location:** `api/middleware.py:27`
* **Severity:** `LOW`
* **Classification:** **`FALSE_POSITIVE`**

**Portal Justification:**
> This finding is a false positive decoy generated from the default hackathon assessment template. The cited file path (api/middleware.py) does not exist in the allocated VulnLab PHP repository. Because this file and code sink are completely absent from the codebase, this finding has zero impact and cannot be exploited.

**Optional Evidence:**
> `Path verification: File 'api/middleware.py' does not exist. There is no Python WSGI/ASGI middleware layer in this PHP-based application.`

---

### Finding #18 · CAPTCHA Bypass via Client-Controlled Parameters

* **Finding ID:** `a1d4d23b-a577-4bdf-865a-81ea9d657634`
* **Location:** `app/lab/captcha-bypass/bypass/index.php:43`
* **Severity:** `MEDIUM`
* **Classification:** **`TRUE_POSITIVE`**

**Portal Justification:**
> The CAPTCHA validation expects the client to supply both the operands (num1, num2) and the computed result in the POST payload. An attacker can tamper with the operands to force trivial calculations (e.g. 1+1=2) or bypass the verification logic entirely (CWE-807).

**Optional Evidence:**
> `app/lab/captcha-bypass/bypass/index.php:43 — if($_POST['result'] == $_POST['num1'] + $_POST['num2']) (Both operands and result are sent from and controlled by client POST)`

---

### Finding #19 · OS Command Injection in Ping Utility

* **Finding ID:** `576a4228-d955-4fb0-b025-6a22a231319a`
* **Location:** `app/lab/command-injection/ping-low/index.php:44`
* **Severity:** `CRITICAL`
* **Classification:** **`TRUE_POSITIVE`**

**Portal Justification:**
> The ping utility executes the system ping binary using exec("ping -c5 $input", $out) with raw user input from $_POST["ip"]. Due to the complete absence of input validation or escapeshellarg() sanitization, an attacker can append command chaining operators to execute arbitrary system commands (CWE-78).

**Optional Evidence:**
> `app/lab/command-injection/ping-low/index.php:40 — exec("ping -c5 " . $_POST['ip'], $out); (Unsanitized POST parameter passed directly to system exec sink)`

---

### Finding #20 · ReDoS in email validator

* **Finding ID:** `96a00caf-5ecd-44b1-95f6-3ee015e7ee2c`
* **Location:** `api/validate.py:17`
* **Severity:** `LOW`
* **Classification:** **`FALSE_POSITIVE`**

**Portal Justification:**
> This finding is a false positive decoy generated from the default hackathon assessment template. The cited file path (api/validate.py) does not exist in the allocated VulnLab PHP repository. Because this file and code sink are completely absent from the codebase, this finding has zero impact and cannot be exploited.

**Optional Evidence:**
> `Path verification: File 'api/validate.py' does not exist in target repository. No regex-based Python email validation module exists.`

---

### Finding #21 · Missing CSRF token on health check

* **Finding ID:** `0bc96159-3e91-4559-bf7d-608dea348c77`
* **Location:** `ops/health.py:8`
* **Severity:** `LOW`
* **Classification:** **`FALSE_POSITIVE`**

**Portal Justification:**
> This finding is a false positive decoy generated from the default hackathon assessment template. The cited file path (ops/health.py) does not exist in the allocated VulnLab PHP repository. Because this file and code sink are completely absent from the codebase, this finding has zero impact and cannot be exploited.

**Optional Evidence:**
> `Path verification: File 'ops/health.py' does not exist in target repository. The repository contains no 'ops/' directory or Python health check endpoint.`

---

