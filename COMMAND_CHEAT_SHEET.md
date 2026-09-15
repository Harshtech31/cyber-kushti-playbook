# CYBER KUSHTI 2026 - COMMAND CHEAT SHEET

Run only inside authorised competition scope. Save raw output under scans or evidence and note target/commit/time.

## Start and Integrity

~~~bash
source ~/.security-tools/venv/bin/activate
which semgrep codeql osv-scanner gitleaks trivy
git status --short
git rev-parse HEAD
git log -1 --oneline
git diff --stat
rg --files
rg -n "TODO|FIXME|secret|token|password|admin|role|tenant|webhook" .
~~~

**Common failures:** wrong directory, inactive environment, generated/vendor noise, dirty source. Record the limitation; do not silently change the target.

## Static Analysis and Dependencies

~~~bash
semgrep scan --config auto --json --output scans/semgrep.json .
codeql database create codeql-db --language=<language> --source-root .
codeql database analyze codeql-db <query-suite> --format=sarif-latest --output=scans/codeql.sarif
osv-scanner scan source -r . --format json > scans/osv.json
gitleaks detect --source . --report-format json --report-path scans/gitleaks.json
trivy fs --format json --output scans/trivy.json .
syft dir:. -o cyclonedx-json > scans/sbom.json
~~~

**Validate:** affected version, reachable code path, production relevance, exposure, compensating control, and impact. Tool labels are not severity decisions.

## Language-Specific

~~~bash
python -m pip_audit
bandit -r . -f json -o scans/bandit.json
npm audit --json > scans/npm-audit.json
govulncheck ./...
cargo audit
composer audit
~~~

**Common failures:** missing lockfile, incomplete build, private registry, dev-only dependency, or unsupported language version. State coverage rather than guessing.

## HTTP and APIs

~~~bash
curl -i -sS https://<authorised-target>/<path>
curl -sS https://<authorised-target>/<path> | jq .
http -v GET https://<authorised-target>/<path>
~~~

Compare one controlled dimension at a time: unauthenticated versus authorised identity, own object versus other object, expected state versus forbidden state. Save redacted request/response.

## Docker and Local Runtime (14:15 - 15:00 Bootstrapping)

~~~bash
docker compose up -d --build
docker compose ps
docker compose logs -f --tail 100
ss -lntup | grep -E "8080|3000|5000|8000"
curl -I http://localhost:8080
~~~

**Common failures:** port already in use, missing `.env`, database not initialized. Check `docker compose logs <db-container>` for migration errors.

## AI Code Extraction & Chunking (For Prompt Input)

~~~bash
# Extract high-level project directory tree (excluding noise)
tree -I 'node_modules|vendor|.git|dist|build|venv' -L 3 .

# Find all route handlers and controllers
rg --files | grep -E "route|controller|api|handler|middleware"

# Dump clean controller code to clipboard or file for AI prompt feeding
cat src/controllers/authController.* | head -n 300

# Grep for unparameterized SQL or command sinks to feed to AI Devil's Advocate
rg -n "execute\(|query\(|raw\(|eval\(|exec\(|system\(|Popen" src/
~~~

## Process, Network, and Logs

> RULE-DEPENDENT; use only when organisers explicitly authorise monitoring/network operations.

~~~bash
ps auxww
ss -lntup
ss -tp
lsof -nP -i
journalctl -n 200 --no-pager
tail -n 200 <authorised-log>
tcpdump -ni <interface> -c 100
~~~

**Validate:** baseline difference, timestamp correlation, known teammate/organiser activity, process parentage, account, destination, and service impact before containment.

## Git and Secrets Triage

~~~bash
git log --all --oneline
git log -S"<identifier>" --all --oneline
git grep -n "<identifier>"
openssl dgst -sha256 <evidence-file>
~~~

Do not print secret values into chat, reports, or screenshots. Record a redacted location, fingerprint, exposure path, and permission scope instead.

## Core Tool Validation Guide

| Tool | Expected output | What it misses | Validate before reporting | Common failure |
| --- | --- | --- | --- | --- |
| Semgrep | Rule, file, line, code snippet | framework flow, sanitisation, reachability | trace source to sink in the active branch | auto config is noisy or misses custom frameworks |
| CodeQL | SARIF result with path metadata | unbuilt code, unsupported models, runtime controls | inspect database build coverage and actual path | database creation omitted dependencies or generated code |
| Gitleaks | secret-like string and location/history | live status, exposure, permissions | identify capability and whether an attacker can obtain it | examples, fixtures, or revoked values are reported as active |
| OSV-Scanner | package/version/advisory match | reachable use and deployment exposure | confirm lockfile version, vulnerable feature, and impact | manifest without a resolved lockfile gives incomplete coverage |
| Trivy | dependency, filesystem, image, or IaC issue | deployed topology and compensating controls | inspect actual configuration and exposed service path | base-image or dev-only findings dominate triage |
| Syft / Grype | SBOM or package/advisory correlation | completeness of source image and runtime reachability | reconcile SBOM with lockfile/image digest and target use | mutable image tag or missing private packages |

Archive raw JSON/SARIF/SBOM output unchanged. The report should contain the human verdict and a pointer to the raw artifact, not a copied scanner claim.
