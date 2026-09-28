"""
S0NAR — port scanner.

Wraps python-nmap. Runs nmap -sV against each host concurrently,
using a thread pool because nmap is blocking.

Author: LordXapose
Repo:   https://github.com/LordXapose/s0nar
"""

from __future__ import annotations

import shutil
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable

from . import config, ui

try:
    import nmap  # type: ignore
    _NMAP_AVAILABLE = shutil.which("nmap") is not None
except ImportError:
    nmap = None  # type: ignore
    _NMAP_AVAILABLE = False


def is_available() -> bool:
    return _NMAP_AVAILABLE


def scan_ports(
    host: str,
    ports: str = config.DEFAULT_PORTS,
    timing: str = "-T4",
    timeout: int = 300,
) -> list[dict]:
    if not _NMAP_AVAILABLE:
        return []

    nm = nmap.PortScanner()
    try:
        nm.scan(
            hosts=host, ports=ports,
            arguments=f"-sV {timing} --version-light --host-timeout {timeout}s",
        )
    except Exception as e:
        ui.warn(f"nmap error on {host}: {e}")
        return []

    if host not in nm.all_hosts():
        return []

    open_ports: list[dict] = []
    for proto in nm[host].all_protocols():
        for port in nm[host][proto].keys():
            info = nm[host][proto][port]
            if info.get("state") != "open":
                continue
            open_ports.append({
                "port": port,
                "protocol": proto,
                "state": info.get("state", ""),
                "service": info.get("name", ""),
                "product": info.get("product", ""),
                "version": info.get("version", ""),
            })
    open_ports.sort(key=lambda p: p["port"])
    return open_ports


def scan_ports_concurrently(
    hosts: Iterable[str],
    ports: str = config.DEFAULT_PORTS,
    max_workers: int = config.DEFAULT_PORT_WORKERS,
) -> dict[str, list[dict]]:
    hosts = list(hosts)
    if not _NMAP_AVAILABLE:
        ui.warn("nmap not installed — skipping port scan")
        return {h: [] for h in hosts}

    ui.info(f"Port scanning {len(hosts)} hosts with {max_workers} workers...")
    results: dict[str, list[dict]] = {}

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(scan_ports, h, ports): h for h in hosts}
        for fut in futures:
            host = futures[fut]
            try:
                results[host] = fut.result()
            except Exception as e:
                ui.warn(f"scan failed for {host}: {e}")
                results[host] = []
    return results


def classify_service(port_info: dict) -> str:
    port = port_info.get("port")
    if port in config.NON_HTTP_SERVICES:
        return config.NON_HTTP_SERVICES[port]
    return port_info.get("service") or "unknown"