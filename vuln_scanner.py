"""
S0NAR — vulnerability scanner.

Two layers:
  1. Nuclei (optional): deep template-based scanning for critical,
     high, and medium severity findings.
  2. Built-in checks (always run): missing security headers,
     exposed sensitive files, dangerous HTTP methods.

Author: LordXapose
Repo:   https://github.com/LordXapose/s0nar
"""

from __future__ import annotations

import json
import shutil
import subprocess
from typing import Iterable

import requests

from . import config, ui

# Suppress InsecureRequestWarning for self-signed certs
try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except Exception:
    pass


def nuclei_available() -> bool:
    return shutil.which("nuclei") is not None


# ─────────────────────────────────────────────────────────────────────
# Nuclei wrapper
# ─────────────────────────────────────────────────────────────────────

def run_nuclei(
    url: str,
    severity: str = "critical,high,medium",
    timeout: int = 300,
) -> list[dict]:
    """Run nuclei against a single URL, return parsed JSON findings."""
    if not nuclei_available():
        return []

    try:
        result = subprocess.run(
            [
                "nuclei",
                "-u", url,
                "-json", "-silent",
                "-severity", severity,
                "-timeout", "10",
                "-retries", "1",
                "-no-color",
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        ui.warn(f"nuclei timed out on {url}")
        return []
    except Exception as e:
        ui.warn(f"nuclei error: {e}")
        return []

    findings: list[dict] = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            findings.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return findings


# ─────────────────────────────────────────────────────────────────────
# Built-in checks
# ─────────────────────────────────────────────────────────────────────

def _check_headers(url: str, headers: dict) -> list[dict]:
    findings = []
    for hdr, message in config.SECURITY_HEADERS.items():
        if hdr not in headers:
            findings.append({
                "severity": "medium" if "HSTS" in hdr or "CSP" in hdr else "low",
                "type":     "missing-header",
                "name":     f"Missing {hdr}",
                "url":      url,
                "detail":   message,
            })
    return findings


def _check_sensitive_paths(url: str, timeout: int = 5) -> list[dict]:
    findings = []
    base = url.rstrip("/")
    for path in config.SENSITIVE_PATHS:
        test_url = f"{base}{path}"
        try:
            resp = requests.get(
                test_url,
                timeout=timeout,
                headers={"User-Agent": config.USER_AGENT},
                verify=False,
                allow_redirects=False,
            )
        except Exception:
            continue
        if resp.status_code == 200 and len(resp.content) > 0:
            findings.append({
                "severity": "high",
                "type":     "exposed-file",
                "name":     f"Exposed {path}",
                "url":      test_url,
                "detail":   f"HTTP 200 with {len(resp.content)} bytes",
            })
    return findings


def _check_http_methods(url: str, timeout: int = 5) -> list[dict]:
    findings = []
    for method in config.HTTP_METHODS_TO_CHECK:
        try:
            resp = requests.request(
                method,
                url,
                timeout=timeout,
                headers={"User-Agent": config.USER_AGENT},
                verify=False,
                allow_redirects=False,
            )
        except Exception:
            continue
        # TRACE/OPTIONS returning 200 is a finding
        if resp.status_code == 200:
            findings.append({
                "severity": "low",
                "type":     "http-method",
                "name":     f"{method} method enabled",
                "url":      url,
                "detail":   f"Server responded {resp.status_code}",
            })
    return findings


def builtin_checks(url: str) -> list[dict]:
    """All built-in checks against a single URL."""
    findings: list[dict] = []

    try:
        resp = requests.get(
            url,
            timeout=config.DEFAULT_HTTP_TIMEOUT,
            headers={"User-Agent": config.USER_AGENT},
            verify=False,
            allow_redirects=True,
        )
    except Exception:
        return findings

    findings.extend(_check_headers(url, dict(resp.headers)))
    findings.extend(_check_sensitive_paths(url))
    findings.extend(_check_http_methods(url))
    return findings


# ─────────────────────────────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────────────────────────────

def scan_vulnerabilities(
    live_hosts: Iterable[dict],
    severity: str = "critical,high,medium",
    use_nuclei: bool = True,
) -> list[dict]:
    """
    Scan all live HTTP/HTTPS endpoints.

    live_hosts: list of prober result dicts (must contain 'url').
    """
    live_hosts = [h for h in live_hosts if h.get("url")]
    if not live_hosts:
        return []

    run_nuclei_flag = use_nuclei and nuclei_available()
    if use_nuclei and not run_nuclei_flag:
        ui.warn("nuclei not installed — running built-in checks only")

    all_findings: list[dict] = []

    for host in live_hosts:
        url = host["url"]

        # ── Nuclei ──
        if run_nuclei_flag:
            nuc = run_nuclei(url, severity=severity)
            for finding in nuc:
                # Normalise Nuclei's schema to our flat shape
                info = finding.get("info", {}) or {}
                all_findings.append({
                    "severity": info.get("severity", "info"),
                    "type":     "nuclei",
                    "name":     info.get("name", "nuclei finding"),
                    "url":      finding.get("matched-at") or url,
                    "detail":   info.get("description", "")[:200],
                    "template": finding.get("template-id", ""),
                })

        # ── Built-in ──
        all_findings.extend(builtin_checks(url))

    # Sort: critical → high → medium → low → info
    sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    all_findings.sort(key=lambda f: sev_order.get(f.get("severity", "info"), 5))
    return all_findings