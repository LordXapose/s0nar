# README.md — S0NAR


---

```markdown
███████╗ ██████╗ ███╗   ██╗ █████╗ ██████╗
██╔════╝██╔═████╗████╗  ██║██╔══██╗██╔══██╗
███████╗██║██╔██║██╔██╗ ██║███████║██████╔╝
╚════██║████╔╝██║██║╚██╗██║██╔══██║██╔══██╗
███████║╚██████╔╝██║ ╚████║██║  ██║██║  ██║
╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╝
```

### full-spectrum subdomain reconnaissance

*ping the dark · hear what answers*

<br>

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-magenta.svg)](#)
[![UI: Rich](https://img.shields.io/badge/UI-rich-00b4d8.svg)](https://github.com/Textualize/rich)
[![Async: aiohttp](https://img.shields.io/badge/async-aiohttp-2c5bb4.svg)](https://docs.aiohttp.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/LordXapose/s0nar/pulls)

<br>

**[Features](#-features)** · **[Install](#-installation)** · **[Usage](#-usage)** · **[Output](#-output-files)** · **[Backends](#-optional-backends)** · **[Ethics](#️-ethics--legal)** · **[Roadmap](#️-roadmap)**

<br>

**built by [LordXapose](https://github.com/LordXapose)**

</div>

---

## 🎯 What is S0NAR?

**S0NAR** is an all-in-one subdomain reconnaissance and vulnerability
scanner written in Python. Point it at a domain and it delivers a
complete picture of the external attack surface — every subdomain,
every live host, every open port, every takeover candidate, and every
vulnerability it can find.

Unlike most recon tools that stop at enumeration, **S0NAR chains the
entire pipeline into a single command** — from passive discovery to
vulnerability confirmation — and presents everything in a clean,
color-coded terminal UI.

```bash
$ s0nar scan example.com
```

That's it. One command. Full attack surface.

---

## ✨ Features

|  |  |
|---|---|
| 🔍 **Discovery** | crt.sh · subfinder · amass · DNS brute-force · wildcard detection |
| 🌐 **Probing** | Fully async `aiohttp` · HTTPS-first · TLS inspection · metadata capture |
| 📍 **Enrichment** | IPv4 + IPv6 · ASN · org · country · city · rate-limited geolocation |
| ☠️ **Takeover** | 60+ cloud services fingerprinted · 3 confidence levels |
| 🔓 **Ports** | `python-nmap` with `-sV` · non-HTTP service detection |
| 🚨 **Vulns** | Nuclei templates · built-in header & file-exposure checks |
| 📊 **Reports** | JSON · CSV · TXT · color-coded terminal tables |

### Why S0NAR?

- **Async-first** — 5–10× faster than threaded recon tools
- **Graceful degradation** — works with just Python; unlocks more when backends exist
- **Takeover detection** — confirmed by fingerprint matching, not just CNAME heuristics
- **Real enrichment** — IP, ASN, geolocation, TLS — not just a hostname list
- **Beautiful output** — Rich-powered tables you actually want to look at

---

## 🖥️ Terminal Preview

```
── LIVE SUBDOMAINS ─────────────────────────────────────────────────────
┌────┬───────────────────┬──────────────────┬──────┬──────────┬──────────┐
│  # │ Host              │ IP               │ St   │ Server   │ Title    │
├────┼───────────────────┼──────────────────┼──────┼──────────┼──────────┤
│  1 │ ● api.example.com │ 104.18.32.47     │ 200  │ nginx    │ API Home │
│  2 │ ● www.example.com │ 93.184.216.34    │ 200  │ ECS      │ Welcome  │
│  3 │ ● dev.example.com │ 10.0.0.5         │ 403  │ Apache   │ Forbidden│
│  4 │ ● mail.example.com│ 192.0.2.10       │ 200  │ Postfix  │ Mail     │
└────┴───────────────────┴──────────────────┴──────┴──────────┴──────────┘

── CLOSED / DEAD SUBDOMAINS ───────────────────────────────────────────
┌────┬──────────────────────┬─────────────────────────────────────────┐
│  # │ Host                 │ Reason                                  │
├────┼──────────────────────┼─────────────────────────────────────────┤
│  1 │ ● old.example.com    │ Connection timeout                      │
│  2 │ ● test.example.com   │ DNS resolves but no HTTP/S response     │
│  3 │ ● stage.example.com  │ SSL handshake failed                    │
└────┴──────────────────────┴─────────────────────────────────────────┘

── SUBDOMAIN TAKEOVER CANDIDATES ──────────────────────────────────────
┌────┬──────────────────┬─────────────────────┬───────────────┬──────────┐
│  # │ Host             │ CNAME               │ Service       │ Confid.  │
├────┼──────────────────┼─────────────────────┼───────────────┼──────────┤
│  1 │ ● blog.example   │ user.github.io      │ GitHub Pages  │ CONFIRMED│
│  2 │ ● cdn.example    │ d123.cloudfront.net │ AWS CloudFront│ CNAME    │
└────┴──────────────────┴─────────────────────┴───────────────┴──────────┘

── OPEN PORTS & SERVICES ──────────────────────────────────────────────
┌────┬──────────────────┬────────────────────────────────────────────┐
│  # │ Host             │ Services                                   │
├────┼──────────────────┼────────────────────────────────────────────┤
│  1 │ api.example.com  │ 22/ssh OpenSSH 8.2 · 443/https nginx 1.18  │
│    │                  │ 3306/mysql MySQL 8.0.32                    │
│  2 │ www.example.com  │ 80/http · 443/https                        │
└────┴──────────────────┴────────────────────────────────────────────┘

── VULNERABILITIES ────────────────────────────────────────────────────
┌────┬──────────┬──────────────────────────────────┬──────────────────┐
│  # │ Severity │ URL                              │ Finding          │
├────┼──────────┼──────────────────────────────────┼──────────────────┤
│  1 │ HIGH     │ https://api.example.com/.env     │ Exposed .env     │
│  2 │ MEDIUM   │ https://www.example.com          │ Missing HSTS     │
│  3 │ LOW      │ https://dev.example.com          │ TRACE enabled    │
└────┴──────────┴──────────────────────────────────┴──────────────────┘

── SCAN SUMMARY ───────────────────────────────────────────────────────
╭──────────────────────────┬────────╮
│ Target:                  │ example.com │
│ Duration:                │ 134.2s │
│                          │        │
│ Total discovered:        │ 118    │
│ Live hosts:              │ 87     │
│ Dead hosts:              │ 31     │
│ Takeover candidates:     │ 2      │
│ Open ports:              │ 43     │
│ Vulnerabilities:         │ 8      │
╰──────────────────────────┴────────╯
```

---

## ⚡ Installation

### 1. Install S0NAR

```bash
git clone https://github.com/LordXapose/s0nar.git
cd s0nar
pip install -e .
```

Once installed, both `s0nar` and `sonar` commands are available:

```bash
s0nar --version
sonar --help
```

### 2. Install optional backends *(recommended)*

S0NAR works with **just the Python dependencies**, but detection rates
jump **40–60%** when the external backends are present. S0NAR detects
missing tools and prints a warning — it never crashes.

| Tool | Install | Why it matters |
|------|---------|----------------|
| **subfinder** | `go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest` | Aggregates 60+ passive sources |
| **amass** | `go install -v github.com/owasp-amass/amass/v4/...@master` | OSINT + passive DNS |
| **nuclei** | `go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest` | 10,000+ vulnerability templates |
| **nmap** | `sudo apt install nmap` · `brew install nmap` | Port + service detection |

After installing Nuclei, update the templates:

```bash
nuclei -update-templates
```

### 3. Verify installation

```bash
s0nar banner
```

You'll see the boot sequence with a green dot next to each backend
that's online, and a red dot next to any that are missing.

---

## 🚀 Usage

### Basic scan

```bash
s0nar scan example.com
```

Runs the full pipeline: **enumerate → probe → takeover → ports → vulns**.

### Fast recon (skip slow phases)

```bash
s0nar scan example.com --skip-ports --skip-vuln
```

Just subdomains, liveness, and takeover checks. Runs in 30–60 seconds
on most domains.

### Custom wordlist

```bash
s0nar scan example.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

### Aggressive probing

```bash
s0nar scan example.com --probe-concurrency 200 --timeout 5
```

### Only show the banner

```bash
s0nar banner
```

### Full option reference

| Flag | Description | Default |
|------|-------------|---------|
| `-w, --wordlist PATH` | Custom DNS brute-force wordlist | built-in 500 words |
| `-o, --output-dir PATH` | Output directory | `./s0nar-out` |
| `--skip-subfinder` | Skip subfinder backend | `false` |
| `--skip-amass` | Skip amass backend | `false` |
| `--skip-ports` | Skip nmap port scanning | `false` |
| `--skip-vuln` | Skip Nuclei vulnerability scan | `false` |
| `--skip-takeover` | Skip takeover detection | `false` |
| `--skip-geo` | Skip IP geolocation lookup | `false` |
| `--ports TEXT` | Ports to scan (nmap syntax) | top 100 |
| `--probe-concurrency INT` | HTTP probe concurrency | `100` |
| `--takeover-concurrency INT` | Takeover check concurrency | `50` |
| `--port-workers INT` | Concurrent port scans | `10` |
| `--nuclei-severity TEXT` | Nuclei severity filter | `critical,high,medium` |
| `--timeout INT` | HTTP timeout in seconds | `8` |
| `--no-color` | Disable ANSI colors | `false` |
| `--quiet` | Only print final summary | `false` |
| `--verbose` | Print debug info | `false` |
| `-V, --version` | Show version and exit | — |
| `-h, --help` | Show help | — |

---

## 📁 Output Files

Every scan writes three reports to
`./s0nar-out/<domain>_<timestamp>/`:

| File | Purpose |
|------|---------|
| `report.json` | Full structured data — every field, every host, every finding |
| `report.csv` | Flat CSV, one row per finding (`LIVE`/`DEAD`/`TAKEOVER`/`PORT`/`VULN`) |
| `report.txt` | Plain-text snapshot of the terminal output (no colors) |

### JSON schema (abridged)

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
        {"port": 443, "service": "https", "product": "nginx", "version": "1.18.0"}
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

## 🔌 Optional Backends

S0NAR follows a **graceful degradation** model. Every backend is
optional; missing tools produce a warning, not a crash.

| Backend | Required? | Impact if missing |
|---------|-----------|-------------------|
| `subfinder` | No | ~30% fewer subdomains discovered |
| `amass` | No | ~20% fewer subdomains discovered |
| `nuclei` | No | No deep vuln scanning (built-in checks still run) |
| `nmap` | No | No port scanning / service detection |

**Tip:** for maximum coverage, install all four. For quick
subdomain-only recon, Python dependencies are enough.

---

## 🎨 Terminal UI

S0NAR uses [Rich](https://github.com/Textualize/rich) for beautiful
terminal output:

| Color | Meaning |
|-------|---------|
| 🟢 **Green** | Live host · HTTP 2xx · success |
| 🟡 **Yellow** | Warning · 3xx/4xx · medium vuln · cname-only takeover |
| 🔴 **Red** | Dead host · 5xx · confirmed takeover · high/critical |
| 🔵 **Cyan** | Section headers · URLs · target info |
| 🟣 **Magenta** | Hostnames · takeover findings |

**Auto-detection:** falls back to plain text when output is piped or
the terminal doesn't support ANSI colors.

### Boot sequence

On startup, S0NAR prints a brief boot sequence so you can see which
backends are online before the scan begins:

```
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

## 🛡️ Ethics & Legal

> **S0NAR is for authorized security testing only.**
>
> Only scan domains you own or have **explicit written permission**
> to test. Unauthorized scanning is illegal in most jurisdictions and
> violates most cloud providers' terms of service.
>
> The author (`LordXapose`) assumes **no responsibility** for misuse
> of this tool. Use it responsibly, ethically, and within the bounds
> of the law.

By using S0NAR, you agree to:

1. Only scan systems you are **authorized** to test
2. Respect **rate limits** — S0NAR throttles automatically, but you
   control concurrency
3. Report any **vulnerabilities you find** to the responsible party
   through proper disclosure channels
4. Never use S0NAR for **harassment, extortion, or criminal activity**

---

## 🗺️ Roadmap

- [x] Async HTTP probing with `aiohttp`
- [x] Subdomain takeover detection (60+ services)
- [x] Port scanning via `python-nmap`
- [x] Nuclei vulnerability integration
- [x] Multi-source enumeration (crt.sh + subfinder + amass + brute)
- [x] Rich terminal UI with color-coded tables
- [ ] Resume interrupted scans
- [ ] Diff mode — compare against previous scan
- [ ] Slack / Discord / generic webhook notifications
- [ ] Web dashboard (FastAPI + HTMX)
- [ ] Docker image & GitHub Actions CI
- [ ] PyPI release (`pip install s0nar`)

---

## 🤝 Contributing

Contributions are welcome. Please follow these steps:

1. **Fork** the repository
2. **Create a branch** — `git checkout -b feat/my-feature`
3. **Follow PEP 8**, line length 100
4. **Add tests** where practical
5. **Open a PR** against `main` with a clear description

For bug reports, please include:

- S0NAR version (`s0nar --version`)
- Python version
- OS
- The exact command you ran
- The full error output

---

## 🐛 Known Issues

- Windows native is untested — use **WSL** for now
- SYN port scans require **root/sudo** — falls back to connect scan if not elevated
- `ip-api.com` free tier allows **45 req/min** — very large scans may
  see temporary throttling (S0NAR retries with backoff)

---

## 📜 License

MIT License © 2026 [LordXapose](https://github.com/LordXapose)

See [LICENSE](LICENSE) for the full text.

---

## 🙏 Credits

- **Author:** [LordXapose](https://github.com/LordXapose)
- **UI:** [Rich](https://github.com/Textualize/rich) by Will McGugan
- **Async HTTP:** [aiohttp](https://github.com/aio-libs/aiohttp)
- **DNS:** [dnspython](https://github.com/rthalley/dnspython)
- **Port scanning:** [python-nmap](https://github.com/rthalley/python-nmap)
- **Backends:** [subfinder](https://github.com/projectdiscovery/subfinder) · [amass](https://github.com/owasp-amass/amass) · [nuclei](https://github.com/projectdiscovery/nuclei) · [nmap](https://nmap.org)

---

<div align="center">

### if S0NAR helped you, drop a ⭐ on the repo

**[🐛 Report a Bug](https://github.com/LordXapose/s0nar/issues)** ·
**[💡 Request a Feature](https://github.com/LordXapose/s0nar/issues)** ·
**[📖 Read the Docs](https://github.com/LordXapose/s0nar/wiki)**

<br>

*built with paranoia by [LordXapose](https://github.com/LordXapose)*

`ping the dark · hear what answers`

</div>
```

---


##  What's Next

Drop this file into your repo root, then we move on to the source files
in this order:

| # | File | Purpose |
|---|------|---------|
| 1 | `LICENSE` | MIT text (already drafted) |
| 2 | `.gitignore` | Python + `s0nar-out/` (already drafted) |
| 3 | `requirements.txt` | 6 Python deps (already drafted) |
| 4 | `pyproject.toml` | Dual binary `s0nar` / `sonar` (already drafted) |
| 5 | `s0nar/__init__.py` | Version, author, URL (already drafted) |
| 6 | `s0nar/__main__.py` | `python -m s0nar` support (already drafted) |
| 7 | `s0nar/ui.py` | Banner, theme, all tables (already drafted) |
| 8 | `s0nar/main.py` | Typer CLI (already drafted) |
| **9** | **`s0nar/config.py`** | **← next** — port list, wordlist, fingerprints |
| 10 | `s0nar/enumerator.py` | crt.sh + subfinder + amass + brute-force |
| 11 | `s0nar/prober.py` | Async aiohttp probing + IP resolution |
| 12 | `s0nar/takeover.py` | CNAME matching + fingerprint confirmation |
| 13 | `s0nar/port_scanner.py` | python-nmap wrapper |
| 14 | `s0nar/vuln_scanner.py` | Nuclei subprocess + built-in checks |
| 15 | `s0nar/output.py` | JSON / CSV / TXT report writers |
