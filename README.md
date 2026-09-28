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

---

## 🎯 Overview

**S0NAR** is an all-in-one Python-based subdomain reconnaissance and vulnerability-scanning framework designed to map an organization's external attack surface.

Instead of stopping at subdomain enumeration, S0NAR connects multiple reconnaissance stages into a single workflow:

**Discovery → Probing → Enrichment → Takeover Detection → Port Scanning → Vulnerability Scanning → Reporting**

Point S0NAR at an authorized target:

```bash
s0nar scan example.com
```

and it builds a consolidated view of discovered infrastructure, live hosts, exposed services, potential subdomain takeovers, and detected vulnerabilities.

> **One command. One pipeline. Full attack-surface visibility.**

---

## ✨ Features

| Capability                    | Description                                                          |
| ----------------------------- | -------------------------------------------------------------------- |
| 🔍 **Subdomain Discovery**    | crt.sh, subfinder, amass, DNS brute-force and wildcard detection     |
| 🌐 **HTTP Probing**           | Fully asynchronous `aiohttp` probing with HTTPS-first behavior       |
| 🔐 **TLS Inspection**         | TLS information and certificate-related metadata collection          |
| 📍 **Asset Enrichment**       | IPv4, IPv6, ASN, organization, country and city information          |
| ☁️ **Takeover Detection**     | Fingerprint-based detection across 60+ cloud services                |
| 🔓 **Port Scanning**          | `python-nmap` integration with service/version detection             |
| 🚨 **Vulnerability Scanning** | Nuclei integration plus built-in security checks                     |
| 📊 **Reporting**              | JSON, CSV and TXT output                                             |
| 🎨 **Terminal UI**            | Rich-powered tables, status indicators and scan summaries            |
| ⚙️ **Graceful Degradation**   | Optional external tools do not prevent the core scanner from running |

### Why S0NAR?

* **Async-first architecture** for high-speed HTTP probing.
* **Multi-source discovery** combines passive and active enumeration.
* **Fingerprint-based takeover detection** instead of relying only on CNAME heuristics.
* **Asset enrichment** provides context beyond a simple hostname list.
* **Integrated port and service discovery** through Nmap.
* **Integrated vulnerability scanning** through Nuclei.
* **Structured reports** make scan results easy to process programmatically.
* **Graceful degradation** allows the scanner to operate even when optional backends are unavailable.
* **Rich terminal output** makes large reconnaissance results easier to understand.

---

## 🧩 Reconnaissance Pipeline

```text
                         ┌──────────────────┐
                         │   Target Domain  │
                         └────────┬─────────┘
                                  │
                                  ▼
                     ┌─────────────────────────┐
                     │   Subdomain Discovery   │
                     │ crt.sh / subfinder /    │
                     │ amass / DNS brute-force │
                     └────────────┬────────────┘
                                  │
                                  ▼
                     ┌─────────────────────────┐
                     │     HTTP / TLS Probe    │
                     │   aiohttp + metadata    │
                     └────────────┬────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
             ┌───────────┐ ┌────────────┐ ┌──────────────┐
             │   Asset   │ │ Takeover   │ │     Nmap     │
             │ Enrichment│ │ Detection  │ │ Port Scanning│
             └─────┬─────┘ └─────┬──────┘ └──────┬───────┘
                   │             │               │
                   └─────────────┼───────────────┘
                                 ▼
                     ┌─────────────────────────┐
                     │ Vulnerability Scanning  │
                     │   Nuclei + Built-ins    │
                     └────────────┬────────────┘
                                  │
                                  ▼
                     ┌─────────────────────────┐
                     │       Reporting         │
                     │ JSON / CSV / TXT / CLI  │
                     └─────────────────────────┘
```

---

## 🖥️ Terminal Preview

```text
── LIVE SUBDOMAINS ─────────────────────────────────────────────────────

┌────┬───────────────────┬──────────────────┬──────┬──────────┬──────────┐
│ #  │ Host              │ IP
```
