"""
S0NAR — subdomain enumeration.

Combines four sources:
  1. crt.sh          — certificate transparency logs (free, no key)
  2. subfinder       — optional, aggregates 60+ passive sources
  3. amass           — optional, OSINT + passive DNS
  4. DNS brute-force — wordlist-driven active probing

Every source is deduplicated and the result is filtered against
wildcard DNS to eliminate false positives.

Author: LordXapose
Repo:   https://github.com/LordXapose/s0nar
"""

from __future__ import annotations

import json
import random
import shutil
import socket
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable

from . import config, ui


# ─────────────────────────────────────────────────────────────────────
# Passive source: crt.sh
# ─────────────────────────────────────────────────────────────────────

def _crt_sh(domain: str, timeout: int = 20) -> set[str]:
    """Query crt.sh certificate transparency logs."""
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    req = urllib.request.Request(url, headers={"User-Agent": config.USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
        data = json.loads(raw)
    except Exception as e:
        ui.warn(f"crt.sh failed: {e}")
        return set()

    subs: set[str] = set()
    for entry in data:
        name_value = entry.get("name_value", "")
        for name in name_value.split("\n"):
            name = name.strip().lower().lstrip("*.")
            if name and name.endswith(domain) and name != domain:
                subs.add(name)
    return subs


# ─────────────────────────────────────────────────────────────────────
# Passive source: subfinder (optional)
# ─────────────────────────────────────────────────────────────────────

def _subfinder(domain: str, timeout: int = 180) -> set[str]:
    if shutil.which("subfinder") is None:
        return set()

    try:
        result = subprocess.run(
            ["subfinder", "-d", domain, "-silent", "-all"],
            capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        ui.warn("subfinder timed out")
        return set()
    except Exception as e:
        ui.warn(f"subfinder error: {e}")
        return set()

    subs = set()
    for line in result.stdout.splitlines():
        line = line.strip().lower()
        if line and line.endswith(domain) and line != domain:
            subs.add(line)
    return subs


# ─────────────────────────────────────────────────────────────────────
# Passive source: amass (optional)
# ─────────────────────────────────────────────────────────────────────

def _amass(domain: str, timeout: int = 300) -> set[str]:
    if shutil.which("amass") is None:
        return set()

    try:
        # Passive mode is faster and less intrusive
        result = subprocess.run(
            ["amass", "enum", "-passive", "-d", domain, "-timeout", "5"],
            capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        ui.warn("amass timed out")
        return set()
    except Exception as e:
        ui.warn(f"amass error: {e}")
        return set()

    subs = set()
    for line in result.stdout.splitlines():
        line = line.strip().lower()
        if not line:
            continue
        token = line.split()[0]
        if token.endswith(domain) and token != domain:
            subs.add(token)
    return subs


# ─────────────────────────────────────────────────────────────────────
# Wildcard detection
# ─────────────────────────────────────────────────────────────────────

def _detect_wildcard(domain: str) -> str | None:
    """
    Return the IP that a random non-existent subdomain resolves to,
    or None if no wildcard DNS is in play.
    """
    random_label = f"wildcard-{random.randint(100000, 999999)}"
    probe = f"{random_label}.{domain}"
    try:
        return socket.gethostbyname(probe)
    except socket.gaierror:
        return None


# ─────────────────────────────────────────────────────────────────────
# Active source: DNS brute-force
# ─────────────────────────────────────────────────────────────────────

def _resolve(word: str, domain: str, wildcard_ip: str | None) -> str | None:
    sub = f"{word}.{domain}"
    try:
        ip = socket.gethostbyname(sub)
    except socket.gaierror:
        return None
    if wildcard_ip and ip == wildcard_ip:
        return None
    return sub


def _dns_bruteforce(
    domain: str,
    wordlist: Iterable[str],
    wildcard_ip: str | None,
    threads: int = 50,
) -> set[str]:
    found: set[str] = set()
    with ThreadPoolExecutor(max_workers=threads) as pool:
        futures = [pool.submit(_resolve, w, domain, wildcard_ip) for w in wordlist]
        for f in futures:
            result = f.result()
            if result:
                found.add(result)
    return found


# ─────────────────────────────────────────────────────────────────────
# Wordlist loader
# ─────────────────────────────────────────────────────────────────────

def _load_wordlist(path: str | None) -> list[str]:
    if not path:
        return list(config.BUILTIN_WORDLIST)
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            words = [line.strip() for line in fh if line.strip()
                     and not line.startswith("#")]
        return words
    except FileNotFoundError:
        ui.warn(f"Wordlist not found: {path} — using built-in wordlist")
        return list(config.BUILTIN_WORDLIST)


# ─────────────────────────────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────────────────────────────

def enumerate_subdomains(
    domain: str,
    wordlist_file: str | None = None,
    use_subfinder: bool = True,
    use_amass: bool = True,
    brute_threads: int = 50,
) -> list[str]:
    """
    Run the full enumeration pipeline against `domain`.

    Returns a sorted, deduplicated list of subdomains.
    """
    domain = domain.lower().strip().lstrip(".")
    ui.info(f"Enumerating [cyan]{domain}[/]")

    # ── Wildcard detection first, so brute-force can filter ──
    wildcard_ip = _detect_wildcard(domain)
    if wildcard_ip:
        ui.warn(f"Wildcard DNS detected — {domain} resolves all subdomains to {wildcard_ip}")

    collected: set[str] = set()

    # ── 1. crt.sh ──
    ui.info("Querying crt.sh...")
    crt = _crt_sh(domain)
    ui.success(f"crt.sh: {len(crt)} subdomains")
    collected |= crt

    # ── 2. subfinder ──
    if use_subfinder:
        if shutil.which("subfinder"):
            ui.info("Running subfinder...")
            sf = _subfinder(domain)
            ui.success(f"subfinder: {len(sf)} subdomains")
            collected |= sf
        else:
            ui.warn("subfinder not installed — skipping")

    # ── 3. amass ──
    if use_amass:
        if shutil.which("amass"):
            ui.info("Running amass (passive)...")
            am = _amass(domain)
            ui.success(f"amass: {len(am)} subdomains")
            collected |= am
        else:
            ui.warn("amass not installed — skipping")

    # ── 4. DNS brute-force ──
    words = _load_wordlist(wordlist_file)
    ui.info(f"DNS brute-force with {len(words)} words...")
    brute = _dns_bruteforce(domain, words, wildcard_ip, threads=brute_threads)
    ui.success(f"brute-force: {len(brute)} subdomains")
    collected |= brute

    # ── Filter: keep only names that end with the domain ──
    final = sorted(
        s for s in collected
        if s.endswith(domain) and s != domain and "*" not in s
    )
    ui.success(f"Total unique subdomains: [bold green]{len(final)}[/]")
    return final