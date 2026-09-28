"""
S0NAR — liveness prober.

Async HTTP/HTTPS probing built on aiohttp. For each subdomain we:
  1. Resolve A / AAAA records
  2. Probe HTTPS then HTTP
  3. Capture status, server, title, response time
  4. Optionally enrich with ASN + geolocation

Author: LordXapose
Repo:   https://github.com/LordXapose/s0nar
"""

from __future__ import annotations

import asyncio
import socket
import time
from typing import Iterable

import aiohttp

from . import config, ui


# ─────────────────────────────────────────────────────────────────────
# DNS resolution (sync, run in executor)
# ─────────────────────────────────────────────────────────────────────

def _resolve_ipv4(host: str) -> str | None:
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None


def _resolve_ipv6(host: str) -> str | None:
    try:
        infos = socket.getaddrinfo(host, None, socket.AF_INET6)
        return infos[0][4][0] if infos else None
    except socket.gaierror:
        return None


async def resolve_ip(host: str) -> tuple[str | None, str | None]:
    """Return (ipv4, ipv6), running blocking getaddrinfo in a thread."""
    loop = asyncio.get_event_loop()
    v4, v6 = await asyncio.gather(
        loop.run_in_executor(None, _resolve_ipv4, host),
        loop.run_in_executor(None, _resolve_ipv6, host),
    )
    return v4, v6


# ─────────────────────────────────────────────────────────────────────
# Geolocation (rate-limited, cached)
# ─────────────────────────────────────────────────────────────────────

class GeoCache:
    """
    Token-bucket limiter for ip-api.com (45 req/min) plus an IP → result
    cache so duplicate IPs are queried once.
    """

    def __init__(self, rate_per_min: int = config.GEO_RATE_PER_MIN):
        self._cache: dict[str, dict] = {}
        self._interval = 60.0 / rate_per_min
        self._last_call = 0.0
        self._lock = asyncio.Lock()

    async def lookup(self, session: aiohttp.ClientSession, ip: str) -> dict | None:
        if not ip:
            return None
        if ip in self._cache:
            return self._cache[ip]

        async with self._lock:
            now = time.monotonic()
            wait = self._interval - (now - self._last_call)
            if wait > 0:
                await asyncio.sleep(wait)
            self._last_call = time.monotonic()

        url = config.GEO_API_URL.format(ip=ip)
        try:
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=6)
            ) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                if data.get("status") != "success":
                    return None
                result = {
                    "asn":     data.get("as", "").split()[0] if data.get("as") else "",
                    "org":     data.get("org") or data.get("isp", ""),
                    "country": data.get("country", ""),
                    "city":    data.get("city", ""),
                }
                self._cache[ip] = result
                return result
        except Exception:
            return None


# ─────────────────────────────────────────────────────────────────────
# HTML helpers
# ─────────────────────────────────────────────────────────────────────

def extract_title(html: str) -> str:
    if not html:
        return ""
    lower = html.lower()
    start = lower.find("<title>")
    if start == -1:
        return ""
    end = lower.find("</title>", start)
    if end == -1:
        return ""
    title = html[start + 7:end].strip()
    # collapse whitespace and truncate
    title = " ".join(title.split())
    return title[:80]


# ─────────────────────────────────────────────────────────────────────
# Single-host probe
# ─────────────────────────────────────────────────────────────────────

async def _probe_one(
    session: aiohttp.ClientSession,
    host: str,
    timeout: int,
    geo_cache: GeoCache | None,
) -> dict:
    """
    Probe one host over HTTPS then HTTP. Always returns a dict — never
    raises.
    """
    result: dict = {
        "host":         host,
        "ip":           None,
        "ipv6":         None,
        "asn":          "",
        "org":          "",
        "country":      "",
        "city":         "",
        "url":          None,
        "scheme":       None,
        "status_code":  None,
        "server":       "",
        "title":        "",
        "response_ms":  None,
        "alive":        False,
        "reason":       None,
    }

    # ── DNS ──
    ipv4, ipv6 = await resolve_ip(host)
    result["ip"]   = ipv4
    result["ipv6"] = ipv6

    if not ipv4 and not ipv6:
        result["reason"] = "DNS lookup failed"
        return result

    # ── Geo enrichment ──
    if geo_cache and ipv4:
        geo = await geo_cache.lookup(session, ipv4)
        if geo:
            result.update(geo)

    # ── HTTP probes ──
    for scheme in ("https", "http"):
        url = f"{scheme}://{host}"
        t0 = time.monotonic()
        try:
            # HEAD first (cheap)
            async with session.head(
                url,
                timeout=aiohttp.ClientTimeout(total=timeout),
                allow_redirects=False,
                ssl=False,
            ) as resp:
                status = resp.status
                server = resp.headers.get("Server", "")

                # Fall back to GET if HEAD rejects or returns 4xx/5xx
                if status >= 400 or not server:
                    async with session.get(
                        url,
                        timeout=aiohttp.ClientTimeout(total=timeout),
                        allow_redirects=False,
                        ssl=False,
                    ) as resp2:
                        status = resp2.status
                        server = resp2.headers.get("Server", server)
                        ctype = resp2.headers.get("Content-Type", "")
                        body = await resp2.text(errors="ignore") \
                            if "text/html" in ctype else ""
                else:
                    body = ""

                result.update({
                    "url":         url,
                    "scheme":      scheme,
                    "status_code": status,
                    "server":      server[:60],
                    "title":       extract_title(body),
                    "response_ms": int((time.monotonic() - t0) * 1000),
                    "alive":       True,
                    "reason":      None,
                })
                return result

        except asyncio.TimeoutError:
            result["reason"] = f"{scheme.upper()} timeout"
        except aiohttp.ClientConnectorSSLError:
            result["reason"] = f"{scheme.upper()} SSL handshake failed"
        except aiohttp.ClientConnectorCertificateError:
            result["reason"] = f"{scheme.upper()} certificate error"
        except aiohttp.ClientConnectorError:
            result["reason"] = f"{scheme.upper()} connection refused"
        except aiohttp.ClientError as e:
            result["reason"] = f"{scheme.upper()} {type(e).__name__}"
        except Exception as e:
            result["reason"] = f"{scheme.upper()} {type(e).__name__}"

    # Nothing worked
    if not result["reason"]:
        result["reason"] = "No HTTP/HTTPS response"
    return result


# ─────────────────────────────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────────────────────────────

async def probe_all_async(
    subdomains: Iterable[str],
    concurrency: int = config.DEFAULT_PROBE_CONCURRENCY,
    timeout: int = config.DEFAULT_HTTP_TIMEOUT,
    enrich_geo: bool = True,
) -> list[dict]:
    """
    Probe a list of subdomains concurrently.

    Returns a list of result dicts, one per subdomain, in the same
    order as input.
    """
    subdomains = list(subdomains)
    sem = asyncio.Semaphore(concurrency)
    connector = aiohttp.TCPConnector(
        limit=concurrency,
        limit_per_host=5,            # never hammer a single host
        ssl=False,
        ttl_dns_cache=300,           # cache DNS for 5 minutes
    )
    geo_cache = GeoCache() if enrich_geo else None

    results: list[dict] = [None] * len(subdomains)  # type: ignore

    with ui.make_progress("Probing") as progress:
        task = progress.add_task("Probing", total=len(subdomains))

        async with aiohttp.ClientSession(
            connector=connector,
            headers={"User-Agent": config.USER_AGENT},
        ) as session:

            async def bounded(idx: int, host: str) -> None:
                async with sem:
                    try:
                        results[idx] = await _probe_one(
                            session, host, timeout, geo_cache,
                        )
                    except Exception as e:
                        results[idx] = {
                            "host": host, "alive": False,
                            "reason": f"probe crashed: {type(e).__name__}",
                            "ip": None, "ipv6": None,
                            "asn": "", "org": "", "country": "", "city": "",
                            "url": None, "scheme": None,
                            "status_code": None, "server": "",
                            "title": "", "response_ms": None,
                        }
                    finally:
                        progress.advance(task)

            await asyncio.gather(*[
                bounded(i, h) for i, h in enumerate(subdomains)
            ])

    return results