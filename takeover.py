"""
S0NAR — subdomain takeover detection.

For every subdomain:
  1. Resolve CNAME
  2. Match the target against the fingerprint database
  3. Confirm by fetching the HTTP body and looking for the service's
     "unclaimed" page signature

Confidence levels:
  - confirmed  : CNAME matches AND body fingerprint matched
  - cname-only : CNAME matches but body looked normal
  - dangling   : CNAME matches but nothing responds at all

Author: LordXapose
Repo:   https://github.com/LordXapose/s0nar
"""

from __future__ import annotations

import asyncio
from typing import Iterable

import aiohttp
import dns.asyncresolver

from . import config, ui


def _make_resolver() -> dns.asyncresolver.Resolver:
    resolver = dns.asyncresolver.Resolver(configure=False)
    resolver.nameservers = list(config.DNS_RESOLVERS)
    resolver.timeout  = config.DNS_TIMEOUT
    resolver.lifetime = config.DNS_LIFETIME
    return resolver


async def _get_cname(host: str, resolver: dns.asyncresolver.Resolver) -> str | None:
    try:
        answers = await resolver.resolve(host, "CNAME")
    except Exception:
        return None
    if not answers:
        return None
    return str(answers[0].target).rstrip(".").lower()


def _match_service(cname: str):
    for pattern, (service, fps) in config.TAKEOVER_FINGERPRINTS.items():
        if pattern in cname:
            return pattern, service, fps
    return None


async def _confirm(
    session: aiohttp.ClientSession,
    host: str,
    cname: str,
    service: str,
    fingerprints: list[str],
) -> dict:
    for scheme in ("https", "http"):
        url = f"{scheme}://{host}"
        try:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=8),
                allow_redirects=True,
                ssl=False,
            ) as resp:
                body = await resp.text(errors="ignore")
                body_lower = body.lower()

                for fp in fingerprints:
                    if fp.lower() in body_lower:
                        return {
                            "host":        host,
                            "cname":       cname,
                            "service":     service,
                            "fingerprint": fp,
                            "url":         url,
                            "http_status": resp.status,
                            "confidence":  "confirmed",
                        }

                return {
                    "host":        host,
                    "cname":       cname,
                    "service":     service,
                    "fingerprint": None,
                    "url":         url,
                    "http_status": resp.status,
                    "confidence":  "cname-only",
                }
        except Exception:
            continue

    return {
        "host":        host,
        "cname":       cname,
        "service":     service,
        "fingerprint": None,
        "url":         None,
        "http_status": None,
        "confidence":  "dangling",
    }


async def scan_takeover(
    subdomains: Iterable[str],
    concurrency: int = config.DEFAULT_TAKEOVER_CONCURRENCY,
) -> list[dict]:
    """Check every subdomain for subdomain takeover vulnerability."""
    subdomains = list(subdomains)
    resolver = _make_resolver()
    sem = asyncio.Semaphore(concurrency)

    connector = aiohttp.TCPConnector(limit=concurrency, ssl=False)
    findings: list[dict] = []

    async with aiohttp.ClientSession(
        connector=connector,
        headers={"User-Agent": config.USER_AGENT},
    ) as session:

        async def check(host: str):
            async with sem:
                cname = await _get_cname(host, resolver)
                if not cname:
                    return None
                match = _match_service(cname)
                if not match:
                    return None
                _, service, fps = match
                return await _confirm(session, host, cname, service, fps)

        results = await asyncio.gather(*[check(h) for h in subdomains])
        findings = [r for r in results if r is not None]

    order = {"confirmed": 0, "cname-only": 1, "dangling": 2}
    findings.sort(key=lambda x: (order.get(x["confidence"], 3), x["host"]))
    return findings