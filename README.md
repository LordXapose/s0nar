# S0NAR

```text
 ███████╗ ██████╗ ███╗   ██╗ █████╗ ██████╗
 ██╔════╝██╔═████╗████╗  ██║██╔══██╗██╔══██╗
 ███████╗██║██╔██║██╔██╗ ██║███████║██████╔╝
 ╚════██║████╔╝██║██║╚██╗██║██╔══██║██╔══██╗
 ███████║╚██████╔╝██║ ╚████║██║  ██║██║  ██║
 ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝
```

### Full-Spectrum Subdomain Reconnaissance

> **Ping the dark · hear what answers.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-magenta.svg)](#)
[![UI: Rich](https://img.shields.io/badge/UI-Rich-00b4d8.svg)](https://github.com/Textualize/rich)
[![Async: aiohttp](https://img.shields.io/badge/async-aiohttp-2c5bb4.svg)](https://docs.aiohttp.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/LordXapose/s0nar/pulls)

---

## 📖 Table of Contents

* [Overview](#-overview)
* [Features](#-features)
* [Architecture](#-architecture)
* [Terminal Preview](#-terminal-preview)
* [Installation](#-installation)
* [Usage](#-usage)
* [Command-Line Options](#-command-line-options)
* [Output Files](#-output-files)
* [JSON Schema](#-json-schema)
* [Optional Backends](#-optional-backends)
* [Terminal UI](#-terminal-ui)
* [Responsible Use](#-responsible-use)
* [Roadmap](#-roadmap)
* [Project Structure](#-project-structure)
* [Contributing](#-contributing)
* [Known Issues](#-known-issues)
* [License](#-license)
* [Credits](#-credits)

---

## 🎯 Overview

**S0NAR** is an all-in-one Python-based subdomain reconnaissance and vulnerability scanner designed to provide a consolidated view of an organization's external attack surface.

Instead of stopping at subdomain enumeration, S0NAR connects multiple reconnaissance and assessment stages into a single workflow:

```text
Discovery
    ↓
HTTP / TLS Probing
    ↓
Asset Enrichment
    ↓
Takeover Detection
    ↓
Port & Service Enumeration
    ↓
Vulnerability Scanning
    ↓
Structured Reporting
```

Point S0NAR at an authorized target:

```bash
s0nar scan example.com
```

and the tool builds a comprehensive view of:

* Discovered subdomains
* Live and unreachable hosts
* HTTP response information
* TLS metadata
* IP addresses
* ASN and organization information
* Geographic information
* Potential subdomain takeovers
* Open ports
* Detected services and versions
* Vulnerability findings
* Structured scan results

### One command. One pipeline. Full attack-surface visibility.

---

## ✨ Features

| Capability                    | Description                                                       |
| ----------------------------- | ----------------------------------------------------------------- |
| 🔍 **Subdomain Discovery**    | crt.sh, subfinder, amass, DNS brute-force and wildcard detection  |
| 🌐 **HTTP Probing**           | Fully asynchronous `aiohttp` probing with HTTPS-first behavior    |
| 🔐 **TLS Inspection**         | TLS inspection and metadata collection                            |
| 📍 **Asset Enrichment**       | IPv4, IPv6, ASN, organization, country and city information       |
| ☁️ **Takeover Detection**     | Fingerprint-based detection across 60+ cloud services             |
| 🔓 **Port Scanning**          | `python-nmap` integration with service/version detection          |
| 🚨 **Vulnerability Scanning** | Nuclei integration plus built-in security checks                  |
| 📊 **Reporting**              | JSON, CSV and TXT reports                                         |
| 🎨 **Terminal UI**            | Rich-powered tables and color-coded findings                      |
| ⚙️ **Graceful Degradation**   | Optional backends fail gracefully instead of crashing the scanner |

### Discovery

S0NAR combines multiple discovery sources:

* `crt.sh`
* `subfinder`
* `amass`
* DNS brute-force
* Wildcard detection

The goal is to reduce dependency on a single enumeration source and provide broader external attack-surface coverage.

### HTTP Probing

Discovered hosts are asynchronously probed using `aiohttp`.

The probing stage collects information such as:

* HTTP/HTTPS availability
* Status codes
* Server information
* Page titles
* Response time
* TLS-related metadata

### Asset Enrichment

Hosts can be enriched with network and geographic information:

* IPv4
* IPv6
* ASN
* Organization
* Country
* City

### Subdomain Takeover Detection

S0NAR fingerprints cloud-hosted services and checks for potential takeover conditions.

The detection system supports:

* 60+ cloud services
* CNAME analysis
* Service fingerprinting
* Multiple confidence levels

Unlike a simple CNAME check, S0NAR attempts to confirm the service fingerprint before classifying a takeover candidate.

### Port & Service Discovery

S0NAR integrates with Nmap through `python-nmap`.

The port-scanning stage can identify:

* Open ports
* Protocols
* Services
* Products
* Service versions

### Vulnerability Scanning

S0NAR supports Nuclei for template-based vulnerability detection and also includes built-in checks.

Examples include:

* Exposed files
* Security-header issues
* Other lightweight HTTP security checks

### Reporting

Each scan can generate:

* JSON
* CSV
* TXT

This makes results suitable for both human review and further automation.

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │     Target Domain    │
                         │      example.com     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │      Discovery Engine        │
                    │                              │
                    │ crt.sh / subfinder / amass  │
                    │ DNS brute-force / wildcard   │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │       HTTP / TLS Probe       │
                    │                              │
                    │ aiohttp / status / title     │
                    │ server / response / TLS      │
                    └──────────────┬───────────────┘
                                   │
                   ┌───────────────┼───────────────┐
                   │               │               │
                   ▼               ▼               ▼
          ┌─────────────┐ ┌───────────────┐ ┌───────────────┐
          │   Asset     │ │   Takeover     │ │     Nmap      │
          │ Enrichment  │ │   Detection    │ │ Port Scanner  │
          │             │ │                │ │               │
          │ IP / ASN    │ │ CNAME / cloud  │ │ Ports / svc   │
          │ Geo / Org   │ │ fingerprints   │ │ versions      │
          └──────┬──────┘ └───────┬────────┘ └───────┬───────┘
                 │                │                  │
                 └────────────────┼──────────────────┘
                                  │
                                  ▼
                    ┌──────────────────────────────┐
                    │    Vulnerability Scanner    │
                    │                              │
                    │ Nuclei + Built-in Checks    │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │          Reporting            │
                    │                              │
                    │ JSON / CSV / TXT / Terminal │
                    └──────────────────────────────┘
```

---

## 🖥️ Terminal Preview

```text
── LIVE SUBDOMAINS ─────────────────────────────────────────────────────────

┌────┬───────────────────┬──────────────────┬──────┬──────────┬──────────┐
│ #  │ Host              │ IP               │ St   │ Server   │ Title    │
├────┼───────────────────┼──────────────────┼──────┼──────────┼──────────┤
│ 1  │ ● api.example.com │ 104.18.32.47     │ 200  │ nginx    │ API Home │
│ 2  │ ● www.example.com │ 93.184.216.34    │ 200  │ ECS      │ Welcome  │
│ 3  │ ● dev.example.com │ 10.0.0.5         │ 403  │ Apache   │ Forbidden│
│ 4  │ ● mail.example.com│ 192.0.2.10       │ 200  │ Postfix  │ Mail     │
└────┴───────────────────┴──────────────────┴──────┴──────────┴──────────┘


── CLOSED / DEAD SUBDOMAINS ────────────────────────────────────────────────

┌────┬──────────────────────┬─────────────────────────────────────────┐
│ #  │ Host                 │ Reason                                  │
├────┼──────────────────────┼─────────────────────────────────────────┤
│ 1  │ ● old.example.com    │ Connection timeout                      │
│ 2  │ ● test.example.com   │ DNS resolves but no HTTP/S response     │
│ 3  │ ● stage.example.com  │ SSL handshake failed                    │
└────┴──────────────────────┴─────────────────────────────────────────┘


── SUBDOMAIN TAKEOVER CANDIDATES ──────────────────────────────────────────

┌────┬──────────────────┬─────────────────────┬───────────────┬──────────┐
│ #  │ Host             │ CNAME               │ Service       │ Confid.  │
├────┼──────────────────┼─────────────────────┼───────────────┼──────────┤
│ 1  │ ● blog.example   │ user.github.io      │ GitHub Pages  │ CONFIRMED│
│ 2  │ ● cdn.example    │ d123.cloudfront.net │ AWS CloudFront│ CNAME    │
└────┴──────────────────┴─────────────────────┴───────────────┴──────────┘


── OPEN PORTS & SERVICES ─────────────────────────────────────────────────

┌────┬──────────────────┬────────────────────────────────────────────┐
│ #  │ Host             │ Services                                   │
├────┼──────────────────┼────────────────────────────────────────────┤
│ 1  │ api.example.com  │ 22/ssh OpenSSH 8.2 · 443/https nginx 1.18│
│    │                  │ 3306/mysql MySQL 8.0.32                    │
│ 2  │ www.example.com  │ 80/http · 443/https                        │
└────┴──────────────────┴────────────────────────────────────────────┘


── VULNERABILITIES ───────────────────────────────────────────────────────

┌────┬──────────┬──────────────────────────────────┬──────────────────┐
│ #  │ Severity │ URL                              │ Finding          │
├────┼──────────┼──────────────────────────────────┼──────────────────┤
│ 1  │ HIGH     │ https://api.example.com/.env     │ Exposed .env     │
│ 2  │ MEDIUM   │ https://www.example.com          │ Missing HSTS     │
│ 3  │ LOW      │ https://dev.example.com          │ TRACE enabled    │
└────┴──────────┴──────────────────────────────────┴──────────────────┘


── SCAN SUMMARY ───────────────────────────────────────────────────────────

╭──────────────────────────┬────────────╮
│ Target:                  │ example.com│
│ Duration:                │ 134.2s     │
│                          │            │
│ Total discovered:        │ 118        │
│ Live hosts:              │ 87         │
│ Dead hosts:              │ 31         │
│ Takeover candidates:     │ 2          │
│ Open ports:              │ 43         │
│ Vulnerabilities:         │ 8          │
╰──────────────────────────┴────────────╯
```

---

# ⚡ Installation

## 1. Clone the repository

```bash
git clone https://github.com/LordXapose/s0nar.git
cd s0nar
```

## 2. Install S0NAR

```bash
pip install -e .
```

Once installed, both commands are available:

```bash
s0nar --version
sonar --help
```

---

## 3. Install Optional Backends

S0NAR can run with its Python dependencies alone, but external backends provide additional discovery and scanning capabilities.

S0NAR detects missing backends and reports their status instead of terminating the scan.

### subfinder

```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

**Purpose:** Passive subdomain enumeration from multiple sources.

### amass

```bash
go install -v github.com/owasp-amass/amass/v4/...@master
```

**Purpose:** OSINT and passive DNS enumeration.

### nuclei

```bash
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

**Purpose:** Template-based vulnerability scanning.

Update Nuclei templates:

```bash
nuclei -update-templates
```

### nmap

Ubuntu/Debian:

```bash
sudo apt install nmap
```

macOS:

```bash
brew install nmap
```

Windows users should install Nmap separately and ensure the executable is available to the application.

---

## 4. Verify the installation

```bash
s0nar banner
```

The startup sequence reports which backends are available.

Example:

```text
▸ initializing s0nar engine...
▸ loading fingerprint database...
▸   ↳ 63 services loaded
▸ loading dns resolver pool...
▸   ↳ 8.8.8.8 · 1.1.1.1 · 9.9.9.9
▸ loading nmap service definitions...
▸   ↳ 14,000+ signatures ready
▸ checking subfinder / amass / nuclei...
▸    ● subfinder  ● amass  ● nuclei  ○ nmap

▸ system armed.
```

---

# 🚀 Usage

## Basic Scan

```bash
s0nar scan example.com
```

The full pipeline runs:

```text
enumerate → probe → takeover → ports → vulnerabilities
```

---

## Fast Reconnaissance

For faster reconnaissance, skip the slower port and vulnerability phases:

```bash
s0nar scan example.com --skip-ports --skip-vuln
```

This focuses on:

* Subdomain discovery
* HTTP probing
* Liveness checks
* Takeover detection

---

## Custom DNS Wordlist

```bash
s0nar scan example.com \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

---

## Aggressive HTTP Probing

Increase HTTP concurrency and reduce the request timeout:

```bash
s0nar scan example.com \
  --probe-concurrency 200 \
  --timeout 5
```

Use concurrency responsibly and respect target-side rate limits.

---

## Banner

Display the S0NAR startup banner without performing a scan:

```bash
s0nar banner
```

---

## Version

```bash
s0nar --version
```

---

## Help

```bash
s0nar --help
```

---

# ⚙️ Command-Line Options

| Option                       | Description                     | Default                |
| ---------------------------- | ------------------------------- | ---------------------- |
| `-w, --wordlist PATH`        | Custom DNS brute-force wordlist | Built-in 500 words     |
| `-o, --output-dir PATH`      | Output directory                | `./s0nar-out`          |
| `--skip-subfinder`           | Skip subfinder                  | `false`                |
| `--skip-amass`               | Skip amass                      | `false`                |
| `--skip-ports`               | Skip Nmap port scanning         | `false`                |
| `--skip-vuln`                | Skip vulnerability scanning     | `false`                |
| `--skip-takeover`            | Skip takeover detection         | `false`                |
| `--skip-geo`                 | Skip IP geolocation             | `false`                |
| `--ports TEXT`               | Ports to scan using Nmap syntax | Top 100                |
| `--probe-concurrency INT`    | HTTP probe concurrency          | `100`                  |
| `--takeover-concurrency INT` | Takeover-check concurrency      | `50`                   |
| `--port-workers INT`         | Concurrent port scans           | `10`                   |
| `--nuclei-severity TEXT`     | Nuclei severity filter          | `critical,high,medium` |
| `--timeout INT`              | HTTP timeout in seconds         | `8`                    |
| `--no-color`                 | Disable ANSI colors             | `false`                |
| `--quiet`                    | Print only the final summary    | `false`                |
| `--verbose`                  | Print debug information         | `false`                |
| `-V, --version`              | Show version and exit           | —                      |
| `-h, --help`                 | Show help and exit              | —                      |

---

# 📁 Output Files

Each scan creates a timestamped output directory:

```text
s0nar-out/
└── example.com_20260928_143201/
    ├── report.json
    ├── report.csv
    └── report.txt
```

## JSON

`report.json` contains the complete structured scan dataset.

It is intended for:

* Programmatic processing
* Automation
* Historical storage
* Integration with other security tooling

## CSV

`report.csv` provides a flattened representation of findings.

Records can represent:

```text
LIVE
DEAD
TAKEOVER
PORT
VULN
```

## TXT

`report.txt` contains a plain-text representation of the terminal output without ANSI colors.

---

# 📦 JSON Schema

A simplified example:

```json
{
  "domain": "example.com",
  "scan_start": "2026-09-28T14:32:01Z",
  "scan_end": "2026-09-28T14:34:15Z",
  "duration_seconds": 134.2,
  "subdomains": [
    {
      "host": "api.example.com",
      "ip": "104.18.32.47",
      "ipv6": null,
      "cname": null,
      "asn": "AS13335",
      "org": "Cloudflare, Inc.",
      "country": "US",
      "city": "San Francisco",
      "http": {
        "url": "https://api.example.com",
        "status_code": 200,
        "server": "nginx/1.18.0",
        "title": "API Home",
        "response_ms": 142
      },
      "ports": [
        {
          "port": 443,
          "service": "https",
          "product": "nginx",
          "version": "1.18.0"
        }
      ],
      "takeover": null,
      "vulnerabilities": [
        {
          "severity": "high",
          "name": "Exposed .env file",
          "url": "https://api.example.com/.env"
        }
      ]
    }
  ]
}
```

---

# 🔌 Optional Backends

S0NAR follows a **graceful degradation** architecture.

Every external backend is optional.

If a backend is unavailable, S0NAR reports the missing dependency and continues with the functionality that remains available.

| Backend     | Required? | Impact if Missing                           |
| ----------- | --------: | ------------------------------------------- |
| `subfinder` |        No | Reduced passive subdomain coverage          |
| `amass`     |        No | Reduced OSINT/passive DNS coverage          |
| `nuclei`    |        No | No Nuclei-based deep vulnerability scanning |
| `nmap`      |        No | No port/service scanning                    |

### Recommended setup

For maximum functionality, install:

```text
subfinder
amass
nuclei
nmap
```

For lightweight subdomain reconnaissance, the Python dependencies are sufficient.

---

# 🎨 Terminal UI

S0NAR uses **Rich** for terminal rendering.

The interface provides structured tables for:

* Live hosts
* Dead hosts
* Takeover candidates
* Open ports
* Vulnerabilities
* Scan summaries

## Status Indicators

| Indicator      | Meaning                                                   |
| -------------- | --------------------------------------------------------- |
| 🟢 **Green**   | Live host, HTTP 2xx, successful operation                 |
| 🟡 **Yellow**  | Warning, 3xx/4xx, medium finding, CNAME-only candidate    |
| 🔴 **Red**     | Dead host, 5xx, confirmed takeover, high/critical finding |
| 🔵 **Cyan**    | Section headers, URLs and target information              |
| 🟣 **Magenta** | Hostnames and takeover findings                           |

### Automatic fallback

If the terminal does not support ANSI color or output is piped to another process, S0NAR automatically falls back to plain text.

---

# 🛡️ Responsible Use

> **S0NAR is intended for authorized security testing only.**

Only scan domains and systems that you own or have explicit permission to assess.

Unauthorized scanning may violate:

* Applicable laws
* Contracts
* Cloud-provider policies
* Bug-bounty program rules
* Network-owner policies

By using S0NAR, you agree to:

1. Scan only systems you are authorized to test.
2. Respect target-side rate limits.
3. Configure concurrency responsibly.
4. Report vulnerabilities through appropriate disclosure channels.
5. Never use S0NAR for harassment, extortion or criminal activity.

The author assumes no responsibility for misuse of the software.

---

# 🗺️ Roadmap

## Reconnaissance

* [x] crt.sh integration
* [x] subfinder integration
* [x] amass integration
* [x] DNS brute-force enumeration
* [x] Wildcard detection
* [x] Async HTTP probing
* [x] TLS inspection
* [x] IPv4/IPv6 resolution
* [x] ASN enrichment
* [x] Geographic enrichment

## Takeover Detection

* [x] CNAME analysis
* [x] Cloud-service fingerprinting
* [x] 60+ service fingerprints
* [x] Multiple confidence levels

## Network Enumeration

* [x] Nmap integration
* [x] Port discovery
* [x] Service detection
* [x] Version detection

## Vulnerability Detection

* [x] Nuclei integration
* [x] Built-in HTTP checks
* [x] Security-header checks
* [x] File-exposure checks

## Reporting

* [x] JSON reports
* [x] CSV reports
* [x] TXT reports
* [x] Rich terminal summaries

## Planned

* [ ] Resume interrupted scans
* [ ] Historical scan storage
* [ ] Diff mode
* [ ] Asset change monitoring
* [ ] Confidence scoring for conflicting scan results
* [ ] Slack notifications
* [ ] Discord notifications
* [ ] Generic webhook support
* [ ] FastAPI web dashboard
* [ ] HTMX interface
* [ ] Docker image
* [ ] GitHub Actions CI
* [ ] PyPI release
* [ ] Automated regression tests
* [ ] Configurable scan profiles

---

# 🧠 Planned Intelligence Layer

A future version of S0NAR can move beyond simple enumeration and begin tracking how the attack surface changes over time.

### Asset Change Monitoring

Compare the current scan with previous scans to detect:

```text
NEW SUBDOMAIN
REMOVED SUBDOMAIN
NEW IP
CHANGED IP
NEW PORT
CLOSED PORT
SERVICE CHANGE
TLS CHANGE
NEW TAKEOVER CANDIDATE
NEW VULNERABILITY
RESOLVED VULNERABILITY
```

Example:

```text
┌───────────────┬────────────┬───────────────────────────┐
│ Change        │ Asset      │ Details                   │
├───────────────┼────────────┼───────────────────────────┤
│ NEW           │ api.example│ Port 8443 detected        │
│ CHANGED       │ dev.example│ IP changed                │
│ NEW           │ cdn.example│ Takeover candidate        │
│ RESOLVED      │ old.example│ Exposed file no longer    │
└───────────────┴────────────┴───────────────────────────┘
```

### Confidence Scoring

Reconnaissance sources can sometimes disagree.

Future versions can assign confidence based on:

* Number of independent sources
* DNS consistency
* HTTP confirmation
* TLS confirmation
* Service fingerprint confidence
* Historical observations

This would allow S0NAR to distinguish between:

```text
CONFIRMED
HIGH CONFIDENCE
MEDIUM CONFIDENCE
LOW CONFIDENCE
UNVERIFIED
```

rather than treating every observation as equally reliable.

---

# 🏗️ Project Structure

```text
s0nar/
│
├── s0nar/
│   ├── __init__.py
│   ├── __main__.py
│   ├── main.py
│   ├── config.py
│   ├── ui.py
│   ├── enumerator.py
│   ├── prober.py
│   ├── takeover.py
│   ├── port_scanner.py
│   ├── vuln_scanner.py
│   └── output.py
│
├── tests/
│
├── s0nar-out/
│
├── requirements.txt
├── pyproject.toml
├── LICENSE
├── .gitignore
└── README.md
```

---

# 🧩 Core Modules

| File              | Responsibility                               |
| ----------------- | -------------------------------------------- |
| `__init__.py`     | Package metadata and version                 |
| `__main__.py`     | `python -m s0nar` support                    |
| `main.py`         | Typer CLI and scan orchestration             |
| `config.py`       | Port lists, wordlists and fingerprints       |
| `ui.py`           | Banner, themes and terminal tables           |
| `enumerator.py`   | crt.sh, subfinder, amass and DNS brute-force |
| `prober.py`       | Async HTTP probing and IP resolution         |
| `takeover.py`     | CNAME matching and fingerprint confirmation  |
| `port_scanner.py` | Nmap integration                             |
| `vuln_scanner.py` | Nuclei subprocess and built-in checks        |
| `output.py`       | JSON, CSV and TXT report generation          |

---

# 🤝 Contributing

Contributions are welcome.

## Development workflow

### 1. Fork the repository

Create your own fork on GitHub.

### 2. Create a feature branch

```bash
git checkout -b feat/my-feature
```

### 3. Follow project conventions

* Follow PEP 8.
* Keep functions focused.
* Add tests where practical.
* Avoid unnecessary dependencies.
* Keep external-tool failures graceful.
* Document significant behavior changes.

### 4. Commit your changes

```bash
git add .
git commit -m "feat: add my feature"
```

### 5. Push the branch

```bash
git push origin feat/my-feature
```

### 6. Open a Pull Request

Open a PR against the `main` branch with a clear description of:

* What changed
* Why it changed
* How it was tested
* Any limitations
* Any new dependencies

---

# 🐛 Bug Reports

When reporting a bug, include:

* S0NAR version

```bash
s0nar --version
```

* Python version
* Operating system
* Exact command used
* Full error output
* Relevant configuration
* Steps to reproduce

A minimal reproducible example is strongly preferred.

---

# ⚠️ Known Issues

### Windows

Windows native operation is currently untested.

WSL may provide a more consistent environment for the external security-tooling stack.

### Nmap privileges

SYN-based scans may require elevated privileges.

When elevated privileges are unavailable, Nmap may fall back to a connect-based scan depending on configuration.

### Geolocation rate limits

The free `ip-api.com` tier has a rate limit of approximately 45 requests per minute.

Large scans may therefore experience temporary throttling.

S0NAR retries requests with backoff where applicable.

---

# 📜 License

```text
MIT License

Copyright (c) 2026 LordXapose
```

See [`LICENSE`](LICENSE) for the complete license text.

---

# 🙏 Credits

S0NAR would not be possible without the open-source projects it integrates with.

### Core dependencies

* **Rich** — terminal UI
* **aiohttp** — asynchronous HTTP client
* **dnspython** — DNS resolution
* **python-nmap** — Python interface to Nmap

### External security tools

* **subfinder** — passive subdomain enumeration
* **amass** — attack-surface and OSINT enumeration
* **Nuclei** — vulnerability scanning
* **Nmap** — network and service discovery

---

# ⭐ Support the Project

If S0NAR is useful to you, consider:

⭐ Starring the repository
🐛 Reporting bugs
💡 Requesting features
🔧 Contributing improvements
📖 Improving the documentation

---

<div align="center">

### S0NAR

```text
ping the dark · hear what answers
```

**Built with paranoia.**

[🐛 Report a Bug](https://github.com/LordXapose/s0nar/issues) ·
[💡 Request a Feature](https://github.com/LordXapose/s0nar/issues) ·
[📖 Documentation](https://github.com/LordXapose/s0nar/wiki)

<br>

**© 2026 LordXapose · MIT License**

</div>
