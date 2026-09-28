# s0nar 
```
 ███████╗ ██████╗ ███╗   ██╗ █████╗ ██████╗
 ██╔════╝██╔═████╗████╗  ██║██╔══██╗██╔══██╗
 ███████╗██║██╔██║██╔██╗ ██║███████║██████╔╝
 ╚════██║████╔╝██║██║╚██╗██║██╔══██║██╔══██╗
 ███████║╚██████╔╝██║ ╚████║██║  ██║██║  ██║
 ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝
              ── v1.0.0 ──

        ▓▓ full-spectrum subdomain reconnaissance ▓▓
          ping the dark · hear what answers

  ┌──────────────────────────────────────────────────┐
  │  dev   LordXapose                                 │
  │  repo  github.com/LordXapose/s0nar                │
  │  lic   MIT                                        │
  └──────────────────────────────────────────────────┘
```

### Rich markup version (what it renders in the terminal)

```python
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

console = Console()

# ── ASCII art rendered in cyan → magenta gradient ──
BANNER_ART = r"""
 ███████╗ ██████╗ ███╗   ██╗ █████╗ ██████╗
 ██╔════╝██╔═████╗████╗  ██║██╔══██╗██╔══██╗
 ███████╗██║██╔██║██╔██╗ ██║███████║██████╔╝
 ╚════██║████╔╝██║██║╚██╗██║██╔══██║██╔══██╗
 ███████║╚██████╔╝██║ ╚████║██║  ██║██║  ██║
 ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝
"""

def show_banner():
    console.print()
    console.print(Align.center(Text(BANNER_ART, style="bold cyan")))

    # version line
    console.print(Align.center(
        Text("── v1.0.0 ──", style="dim magenta")
    ))
    console.print()

    # tagline
    console.print(Align.center(
        Text("▓▓ full-spectrum subdomain reconnaissance ▓▓",
             style="bold magenta")
    ))
    console.print(Align.center(
        Text("ping the dark · hear what answers",
             style="italic dim cyan")
    ))
    console.print()

    # credits panel
    credits = Text()
    credits.append("  dev   ", style="dim")
    credits.append("LordXapose", style="bold cyan")
    credits.append("\n  repo  ", style="dim")
    credits.append("github.com/LordXapose/s0nar",
                   style="underline bright_cyan")
    credits.append("\n  lic   ", style="dim")
    credits.append("MIT", style="bold white")

    console.print(Align.center(Panel(
        credits,
        border_style="cyan",
        box=box.ROUNDED,
        padding=(0, 2),
    )))
    console.print()
```

### What it looks like rendered

```
                  ███████╗ ██████╗ ███╗   ██╗ █████╗ ██████╗
                  ██╔════╝██╔═████╗████╗  ██║██╔══██╗██╔══██╗
                  ███████╗██║██╔██║██╔██╗ ██║███████║██████╔╝
                  ╚════██║████╔╝██║██║╚██╗██║██╔══██║██╔══██╗
                  ███████║╚██████╔╝██║ ╚████║██║  ██║██║  ██║
                  ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝
                                    ── v1.0.0 ──

                        ▓▓ full-spectrum subdomain reconnaissance ▓▓
                          ping the dark · hear what answers

                         ╭─────────────────────────────────╮
                         │  dev   LordXapose               │
                         │  repo  github.com/LordXapose/…  │
                         │  lic   MIT                      │
                         ╰─────────────────────────────────╯
```

---

## 🖥️ Startup Screen (with scan-in-progress flavor)

If you want the banner to feel *alive* — printed line by line like a boot sequence — use this variant. It pauses 60 ms between lines and looks like a real recon tool powering up.

```python
import time
from rich.console import Console
from rich.text import Text
from rich.align import Align

console = Console()

def boot_sequence():
    console.clear()
    lines = [
        ("initializing s0nar engine...",      "dim"),
        ("loading fingerprint database...",   "dim"),
        ("  ↳ 63 services loaded",            "green"),
        ("loading dns resolver pool...",      "dim"),
        ("  ↳ 8.8.8.8 · 1.1.1.1 · 9.9.9.9",   "green"),
        ("loading nmap service definitions...","dim"),
        ("  ↳ 14,000+ signatures ready",      "green"),
        ("checking subfinder / amass / nuclei...", "dim"),
        ("  ↳ all backends online",           "green"),
        ("", "dim"),
        ("system armed.",                     "bold red"),
    ]
    for msg, style in lines:
        console.print(f"  [{style}]▸ {msg}[/]" if msg else "")
        time.sleep(0.06)
    console.print()
```

**Rendered output:**
```
  ▸ initializing s0nar engine...
  ▸ loading fingerprint database...
  ▸   ↳ 63 services loaded
  ▸ loading dns resolver pool...
  ▸   ↳ 8.8.8.8 · 1.1.1.1 · 9.9.9.9
  ▸ loading nmap service definitions...
  ▸   ↳ 14,000+ signatures ready
  ▸ checking subfinder / amass / nuclei...
  ▸   ↳ all backends online

  ▸ system armed.
```

Then the main banner prints right after. This gives the tool genuine hacker-tool energy without being cheesy.

---

## 📄 README.md

```markdown
<div align="center">

```
 ███████╗ ██████╗ ███╗   ██╗ █████╗ ██████╗
 ██╔════╝██╔═████╗████╗  ██║██╔══██╗██╔══██╗
 ███████╗██║██╔██║██╔██╗ ██║███████║██████╔╝
 ╚════██║████╔╝██║██║╚██╗██║██╔══██║██╔══██╗
 ███████║╚██████╔╝██║ ╚████║██║  ██║██║  ██║
 ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝
```

**full-spectrum subdomain reconnaissance**
*ping the dark · hear what answers*

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-magenta)]()
[![Made with Rich](https://img.shields.io/badge/UI-rich-cyan)](https://github.com/Textualize/rich)

</div>

---

## What is S0NAR?

**S0NAR** is an all-in-one subdomain reconnaissance and vulnerability
scanner. Point it at a domain and it will:

- 🔍 **Enumerate** subdomains from passive (crt.sh, subfinder, amass)
  and active (DNS brute-force) sources
- 🌐 **Probe** every host over HTTP/HTTPS with async I/O
- 📍 **Enrich** each host with IP, ASN, country, and city
- ☠️ **Detect** subdomain takeover vulnerabilities against 60+
  cloud services
- 🔓 **Scan** open ports and identify non-HTTP services
- 🚨 **Find** vulnerabilities via Nuclei + built-in checks
- 📊 **Report** everything in beautiful color-coded terminal tables

---

## Install

```bash
git clone https://github.com/LordXapose/s0nar.git
cd s0nar
pip install -r requirements.txt
pip install -e .
```

### Optional backends (recommended for best coverage)

```bash
# Subfinder
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Amass
go install -v github.com/owasp-amass/amass/v4/...@master

# Nuclei
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Nmap (system package)
sudo apt install nmap         # Debian / Ubuntu
brew install nmap             # macOS
```

S0NAR detects missing backends and prints a warning — it will
still run with whatever is available.

---

## Usage

```bash
# Full scan
s0nar scan example.com

# Fast recon (skip ports + vuln scan)
s0nar scan example.com --skip-ports --skip-vuln

# Custom wordlist
s0nar scan example.com -w /path/to/wordlist.txt

# Aggressive probing
s0nar scan example.com --probe-concurrency 200

# Save to a custom directory
s0nar scan example.com -o ./my-recon
```

Run `s0nar --help` for the full option list.

---

## Output

Every scan writes three reports to `./s0nar-out/<domain>_<timestamp>/`:

| File | Description |
|------|-------------|
| `report.json` | Full structured data — every host, port, finding |
| `report.csv`  | Flat one-row-per-finding CSV (LIVE/DEAD/TAKEOVER/PORT/VULN) |
| `report.txt`  | Plain-text ASCII tables, terminal output snapshot |

---

## Terminal Preview

```
── LIVE SUBDOMAINS ──────────────────────────────────────────────
┌────┬──────────────────┬─────────────────┬──────┬──────────┬──────────┐
│ #  │ SUBDOMAIN        │ IP              │ CODE │ SERVER   │ TITLE    │
├────┼──────────────────┼─────────────────┼──────┼──────────┼──────────┤
│  1 │ 🟢 api.example.com│ 104.18.32.47   │ 200  │ nginx    │ API Home │
│  2 │ 🟢 www.example.com│ 93.184.216.34  │ 200  │ ECS      │ Welcome  │
│  3 │ 🟡 dev.example.com│ 10.0.0.5       │ 403  │ Apache   │ Forbidden│
└────┴──────────────────┴─────────────────┴──────┴──────────┴──────────┘

── CLOSED / DEAD SUBDOMAINS ─────────────────────────────────────
┌────┬──────────────────────┬─────────────────────────────────┐
│ #  │ SUBDOMAIN            │ REASON                          │
├────┼──────────────────────┼─────────────────────────────────┤
│  1 │ 🔴 old.example.com   │ Connection timeout              │
│  2 │ 🔴 test.example.com  │ DNS resolves but no HTTP/S      │
│  3 │ 🔴 stage.example.com │ SSL handshake failed            │
└────┴──────────────────────┴─────────────────────────────────┘

── SUBDOMAIN TAKEOVER FINDINGS ──────────────────────────────────
┌────────────┬──────────────────┬─────────────────────┬──────────────┐
│ SEVERITY   │ HOST             │ CNAME TARGET        │ SERVICE      │
├────────────┼──────────────────┼─────────────────────┼──────────────┤
│ 🔴 CONFIRM │ blog.example.com │ user.github.io      │ GitHub Pages │
│ 🟡 CNAME   │ cdn.example.com  │ d123.cloudfront.net │ CloudFront   │
└────────────┴──────────────────┴─────────────────────┴──────────────┘
```

---

## Features in Detail

### Subdomain Enumeration
- **crt.sh** — certificate transparency logs (free, no key)
- **subfinder** — passive API aggregation (60+ sources)
- **amass** — passive DNS and OSINT
- **DNS brute-force** — custom wordlist + 500 built-in words
- **Wildcard detection** — filters false positives automatically

### Liveness Probing
- Fully **async** with `aiohttp` — 5–10× faster than threaded
- HTTPS first, HTTP fallback
- Captures status, server header, title, response time
- Reuses one TCP connection pool with DNS caching

### IP & Geolocation Enrichment
- IPv4 and IPv6 resolution
- ASN, organization, country, city via `ip-api.com`
- Token-bucket rate limiter (45 req/min, free tier)
- Cached — duplicate IPs queried only once

### Takeover Detection
- 60+ cloud services fingerprinted
- Three confidence levels: `confirmed`, `cname-only`, `dangling`
- Confirmation by matching the service's "unclaimed" page body

### Port Scanning
- Top 100+ common ports by default
- Service/version detection (`nmap -sV`)
- Non-HTTP services flagged (SSH, MySQL, Redis, RDP, MongoDB…)

### Vulnerability Scanning
- **Nuclei** integration (critical/high/medium by default)
- Built-in checks: missing security headers, exposed files, TRACE

---

## Requirements

- Python 3.9+
- Linux, macOS, or WSL (Windows native untested)
- ~500 MB RAM for typical scans
- Root/sudo recommended for SYN port scans (falls back to connect scan)

---

## Ethics & Legal

> **S0NAR is for authorized security testing only.**
>
> Only scan domains you own or have **explicit written permission**
> to test. Unauthorized scanning is illegal in most jurisdictions
> and violates most cloud providers' terms of service.
>
> The author (`LordXapose`) assumes **no responsibility** for misuse
> of this tool. Use it responsibly.

---

## Roadmap

- [x] Async HTTP probing
- [x] Subdomain takeover detection
- [x] Port scanning
- [x] Nuclei integration
- [ ] Resume interrupted scans
- [ ] Diff mode against previous scans
- [ ] Slack / Discord / webhook notifications
- [ ] Web dashboard (FastAPI + HTMX)
- [ ] Docker image

---

## Contributing

Pull requests welcome. Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Follow PEP 8, line length 100
4. Add tests where practical
5. Open a PR against `main`

---

## License

MIT © [LordXapose](https://github.com/LordXapose)

---

<div align="center">

**built by [LordXapose](https://github.com/LordXapose)**
*if s0nar helped you, drop a ⭐ on the repo*

`ping the dark · hear what answers`

</div>
```

---

## 🏷️ pyproject.toml (for `pip install -e .`)

```toml
[project]
name = "s0nar"
version = "1.0.0"
description = "Full-spectrum subdomain reconnaissance — ping the dark, hear what answers."
authors = [{ name = "LordXapose", email = "you@example.com" }]
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.9"
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "aiohttp>=3.9.0",
    "dnspython>=2.4.0",
    "python-nmap>=0.7.1",
    "requests>=2.31.0",
]

[project.urls]
Homepage = "https://github.com/LordXapose/s0nar"
Repository = "https://github.com/LordXapose/s0nar"
Issues = "https://github.com/LordXapose/s0nar/issues"

[project.scripts]
s0nar = "s0nar.main:app"
sonar = "s0nar.main:app"    # alias — both work

[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"
```

---

##  Summary of What You Got

| Asset | Where |
|-------|-------|
| ASCII banner | `ui.py` → `show_banner()` |
| Boot sequence | `ui.py` → `boot_sequence()` |
| Developer credit | Rendered in banner + README + pyproject |
| Repo link | `github.com/LordXapose/s0nar` (swap if different) |
| README | Full markdown, badges, ethics section, roadmap |
| pyproject.toml | Enables `pip install -e .` and dual binary `s0nar` / `sonar` |

**One question:** what's the actual GitHub repo URL? I assumed `github.com/LordXapose/s0nar` — if it's different (e.g. `github.com/LordXapose/S0NAR` or a different repo name), tell me and I'll update every reference consistently across the banner, README, and pyproject.

Want me to move on to writing **`main.py` with the Typer CLI + Rich help output** next so the banner actually fires when someone runs `s0nar --help`?
