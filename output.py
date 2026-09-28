"""
S0NAR — report writer.

Writes three formats to the output directory:
  - report.json : complete structured data
  - report.csv  : flat one-row-per-finding CSV
  - report.txt  : plain-text ASCII snapshot

Author: LordXapose
Repo:   https://github.com/LordXapose/s0nar
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def make_output_dir(base: Path, domain: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    safe_domain = domain.replace("/", "_").replace(":", "_")
    out = Path(base) / f"{safe_domain}_{stamp}"
    out.mkdir(parents=True, exist_ok=True)
    return out


def _write_json(path: Path, payload: dict) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, default=str, ensure_ascii=False)


def _write_csv(path, live, dead, takeover, ports, vulns) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["type", "host_or_url", "status", "detail"])

        for r in live:
            writer.writerow([
                "LIVE", r["host"], r.get("status_code", ""),
                f"{r.get('url') or ''} | {r.get('server') or ''} | {r.get('title') or ''}",
            ])
        for r in dead:
            writer.writerow(["DEAD", r["host"], "", r.get("reason", "")])
        for t in takeover:
            writer.writerow([
                "TAKEOVER", t["host"], t["confidence"],
                f"{t['cname']} | {t['service']}",
            ])
        for host, port_list in ports.items():
            for p in port_list:
                writer.writerow([
                    "PORT", host, p.get("port"),
                    f"{p.get('service','')} {p.get('product','')} {p.get('version','')}".strip(),
                ])
        for v in vulns:
            writer.writerow([
                "VULN", v.get("url", ""), v.get("severity", ""),
                f"{v.get('name','')} | {v.get('detail','')}",
            ])


def _write_txt(path, domain, live, dead, takeover, ports, vulns, duration) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("=" * 72 + "\n")
        fh.write("S0NAR scan report\n")
        fh.write(f"Domain:   {domain}\n")
        fh.write(f"Duration: {duration:.1f}s\n")
        fh.write(f"Generated: {datetime.now(timezone.utc).isoformat()}\n")
        fh.write("=" * 72 + "\n\n")

        fh.write(f"=== LIVE ({len(live)}) ===\n")
        for r in live:
            fh.write(f"{r['host']:40s}  {r.get('status_code','-'):>4}  "
                     f"{r.get('ip') or '-':15s}  {r.get('title','')[:40]}\n")

        fh.write(f"\n=== DEAD ({len(dead)}) ===\n")
        for r in dead:
            fh.write(f"{r['host']:40s}  {r.get('ip') or '-':15s}  "
                     f"{r.get('reason','')}\n")

        if takeover:
            fh.write(f"\n=== TAKEOVER ({len(takeover)}) ===\n")
            for t in takeover:
                fh.write(f"[{t['confidence'].upper():10s}] {t['host']} -> "
                         f"{t['cname']} ({t['service']})\n")

        if ports:
            fh.write(f"\n=== OPEN PORTS ===\n")
            for host, port_list in ports.items():
                if not port_list:
                    continue
                fh.write(f"{host}\n")
                for p in port_list:
                    prod = " ".join(filter(None, [p.get("product"), p.get("version")]))
                    fh.write(f"  {p['port']:>5}/tcp  {p.get('service',''):15s}  {prod}\n")

        if vulns:
            fh.write(f"\n=== VULNERABILITIES ({len(vulns)}) ===\n")
            for v in vulns:
                fh.write(f"[{v.get('severity','info').upper():8s}] "
                         f"{v.get('url',''):50s}  {v.get('name','')}\n")


def save_reports(
    output_dir: Path,
    domain: str,
    subdomains: list[str],
    live: list[dict],
    dead: list[dict],
    takeover: list[dict],
    ports: dict[str, list[dict]],
    vulns: list[dict],
    duration: float,
) -> dict[str, str]:
    out_dir = make_output_dir(output_dir, domain)

    json_path = out_dir / "report.json"
    csv_path  = out_dir / "report.csv"
    txt_path  = out_dir / "report.txt"

    payload: dict[str, Any] = {
        "domain":           domain,
        "scan_end":         datetime.now(timezone.utc).isoformat(),
        "duration_seconds": round(duration, 2),
        "total_subdomains": len(subdomains),
        "subdomains":       subdomains,
        "live":             live,
        "dead":             dead,
        "takeover":         takeover,
        "ports":            ports,
        "vulnerabilities":  vulns,
    }

    _write_json(json_path, payload)
    _write_csv(csv_path, live, dead, takeover, ports, vulns)
    _write_txt(txt_path, domain, live, dead, takeover, ports, vulns, duration)

    return {
        "dir":  str(out_dir),
        "json": str(json_path),
        "csv":  str(csv_path),
        "txt":  str(txt_path),
    }