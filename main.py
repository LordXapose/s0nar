"""
S0NAR — CLI entry point.

Usage:
  sonar test -d example.com          # full domain scan
  sonar test -p 1.2.3.4              # probe a single IP
  sonar banner                       # show banner
  sonar --version                    # version
"""

from __future__ import annotations

import asyncio
import time
from pathlib import Path
from typing import Optional

import typer

from . import ui

app = typer.Typer(
    name="sonar",
    help="S0NAR — full-spectrum subdomain reconnaissance.",
    add_completion=False,
    rich_markup_mode="rich",
    no_args_is_help=False,
)


# ─────────────────────────────────────────────────────────────────────
# Root callback
# ─────────────────────────────────────────────────────────────────────

@app.callback(invoke_without_command=True)
def _root(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-V", is_eager=True),
    no_color: bool = typer.Option(False, "--no-color"),
) -> None:
    ui.configure(no_color=no_color)

    if version:
        ui.console.print(
            f"[bold cyan]s0nar[/] v[magenta]{ui.VERSION}[/] "
            f"by [cyan]{ui.AUTHOR}[/]"
        )
        ui.console.print(f"[dim]{ui.REPO}[/]")
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        ui.show_banner()
        ui.console.print(ctx.get_help())
        raise typer.Exit()


# ─────────────────────────────────────────────────────────────────────
# banner
# ─────────────────────────────────────────────────────────────────────

@app.command()
def banner() -> None:
    """Display the S0NAR banner and backend status."""
    from shutil import which

    ui.show_banner()
    ui.boot_sequence({
        "subfinder": which("subfinder") is not None,
        "amass":     which("amass")     is not None,
        "nuclei":    which("nuclei")    is not None,
        "nmap":      which("nmap")      is not None,
    })


# ─────────────────────────────────────────────────────────────────────
# test — the main command
# ─────────────────────────────────────────────────────────────────────

@app.command()
def test(
    domain: Optional[str] = typer.Option(
        None, "-d", "--domain",
        help="Target domain (e.g. example.com).",
    ),
    ip: Optional[str] = typer.Option(
        None, "-p", "--ip",
        help="Target IP address (e.g. 1.2.3.4).",
    ),
    wordlist: Optional[Path] = typer.Option(
        None, "-w", "--wordlist",
        help="Custom DNS brute-force wordlist.",
    ),
    output_dir: Path = typer.Option(
        Path("./s0nar-out"), "-o", "--output-dir",
        help="Directory for reports.",
    ),
    ports: str = typer.Option(
        "21,22,25,53,80,110,143,443,445,3306,3389,5432,5900,6379,"
        "8000,8080,8443,8888,9200,27017",
        "--ports",
        help="Ports to scan (nmap syntax).",
    ),
    skip_subfinder: bool = typer.Option(False, "--skip-subfinder"),
    skip_amass:     bool = typer.Option(False, "--skip-amass"),
    skip_ports:     bool = typer.Option(False, "--skip-ports"),
    skip_vuln:      bool = typer.Option(False, "--skip-vuln"),
    skip_takeover:  bool = typer.Option(False, "--skip-takeover"),
    skip_geo:       bool = typer.Option(False, "--skip-geo"),
    fast:           bool = typer.Option(
        False, "--fast",
        help="Shorthand for --skip-ports --skip-vuln --skip-takeover.",
    ),
    probe_concurrency:    int = typer.Option(100, "--probe-concurrency"),
    takeover_concurrency: int = typer.Option(50,  "--takeover-concurrency"),
    port_workers:         int = typer.Option(10,  "--port-workers"),
    nuclei_severity: str = typer.Option(
        "critical,high,medium", "--nuclei-severity",
    ),
    timeout: int = typer.Option(8, "--timeout"),
    quiet:   bool = typer.Option(False, "--quiet"),
    verbose: bool = typer.Option(False, "--verbose"),
) -> None:
    """
    Run a scan against a domain or IP.

    Examples:

      sonar test -d example.com

      sonar test -p 1.2.3.4

      sonar test -d example.com --fast
    """
    # ── Validate target ─────────────────────────────────────────────
    if not domain and not ip:
        ui.error("You must provide a target: use -d <domain> or -p <ip>")
        ui.console.print()
        ui.console.print("[dim]Examples:[/]")
        ui.console.print("  [cyan]sonar test -d example.com[/]")
        ui.console.print("  [cyan]sonar test -p 1.2.3.4[/]")
        raise typer.Exit(1)

    if domain and ip:
        ui.error("Provide either -d or -p, not both.")
        raise typer.Exit(1)

    # --fast is shorthand
    if fast:
        skip_ports = True
        skip_vuln = True
        skip_takeover = True

    if quiet:
        ui.configure(quiet=True)

    target_kind = "domain" if domain else "ip"
    target = (domain or ip).strip().lower()

    # ── Import scan modules ─────────────────────────────────────────
    try:
        from .enumerator import enumerate_subdomains
        from .prober import probe_all_async
        from .takeover import scan_takeover
        from .port_scanner import scan_ports_concurrently
        from .vuln_scanner import scan_vulnerabilities
        from .output import save_reports
    except ImportError as e:
        ui.error(f"Scan modules not available: {e}")
        raise typer.Exit(1)

    ui.show_banner()
    started = time.time()

    # ── IP mode ─────────────────────────────────────────────────────
    if target_kind == "ip":
        asyncio.run(_run_ip_mode(
            ip=target,
            started=started,
            output_dir=output_dir,
            ports=ports,
            timeout=timeout,
            skip_ports=skip_ports,
            skip_vuln=skip_vuln,
            skip_geo=skip_geo,
            port_workers=port_workers,
            nuclei_severity=nuclei_severity,
            probe_all_async=probe_all_async,
            scan_ports_concurrently=scan_ports_concurrently,
            scan_vulnerabilities=scan_vulnerabilities,
            save_reports=save_reports,
        ))
        return

    # ── Domain mode ─────────────────────────────────────────────────
    asyncio.run(_run_domain_mode(
        domain=target,
        started=started,
        wordlist=wordlist,
        output_dir=output_dir,
        ports=ports,
        timeout=timeout,
        skip_subfinder=skip_subfinder,
        skip_amass=skip_amass,
        skip_ports=skip_ports,
        skip_vuln=skip_vuln,
        skip_takeover=skip_takeover,
        skip_geo=skip_geo,
        probe_concurrency=probe_concurrency,
        takeover_concurrency=takeover_concurrency,
        port_workers=port_workers,
        nuclei_severity=nuclei_severity,
        enumerate_subdomains=enumerate_subdomains,
        probe_all_async=probe_all_async,
        scan_takeover=scan_takeover,
        scan_ports_concurrently=scan_ports_concurrently,
        scan_vulnerabilities=scan_vulnerabilities,
        save_reports=save_reports,
    ))


# ─────────────────────────────────────────────────────────────────────
# Domain mode
# ─────────────────────────────────────────────────────────────────────

async def _run_domain_mode(
    domain: str,
    started: float,
    wordlist,
    output_dir,
    ports: str,
    timeout: int,
    skip_subfinder: bool,
    skip_amass: bool,
    skip_ports: bool,
    skip_vuln: bool,
    skip_takeover: bool,
    skip_geo: bool,
    probe_concurrency: int,
    takeover_concurrency: int,
    port_workers: int,
    nuclei_severity: str,
    enumerate_subdomains,
    probe_all_async,
    scan_takeover,
    scan_ports_concurrently,
    scan_vulnerabilities,
    save_reports,
) -> None:

    # 1. Enumerate
    ui.section("PHASE 1 — ENUMERATION")
    subdomains = enumerate_subdomains(
        domain,
        wordlist_file=str(wordlist) if wordlist else None,
        use_subfinder=not skip_subfinder,
        use_amass=not skip_amass,
    )
    if not subdomains:
        ui.error("No subdomains found. Exiting.")
        return

    # 2. Probe
    ui.section("PHASE 2 — LIVENESS PROBING")
    results = await probe_all_async(
        subdomains, concurrency=probe_concurrency,
        timeout=timeout, enrich_geo=not skip_geo,
    )
    live = [r for r in results if r["alive"]]
    dead = [r for r in results if not r["alive"]]
    ui.success(f"Live: {len(live)}  |  Dead: {len(dead)}")

    # 3. Takeover
    takeover_findings = []
    if not skip_takeover:
        ui.section("PHASE 3 — SUBDOMAIN TAKEOVER")
        takeover_findings = await scan_takeover(
            subdomains, concurrency=takeover_concurrency,
        )
        ui.success(f"Candidates: {len(takeover_findings)}")

    # 4. Ports
    port_results = {}
    if not skip_ports:
        ui.section("PHASE 4 — PORT SCANNING")
        port_results = scan_ports_concurrently(
            subdomains, ports=ports, max_workers=port_workers,
        )
        total_open = sum(len(v) for v in port_results.values())
        ui.success(f"Open ports: {total_open}")

    # 5. Vulns
    vulns = []
    if not skip_vuln and live:
        ui.section("PHASE 5 — VULNERABILITY SCANNING")
        vulns = scan_vulnerabilities(live, severity=nuclei_severity)
        ui.success(f"Findings: {len(vulns)}")

    # 6. Tables
    ui.section("LIVE SUBDOMAINS")
    ui.console.print(ui.live_table(live))

    ui.section("CLOSED / DEAD SUBDOMAINS")
    ui.console.print(ui.dead_table(dead))

    if takeover_findings:
        ui.section("SUBDOMAIN TAKEOVER")
        ui.console.print(ui.takeover_table(takeover_findings))

    if port_results:
        port_rows = [{"host": h, "ports": p}
                     for h, p in port_results.items() if p]
        if port_rows:
            ui.section("OPEN PORTS")
            ui.console.print(ui.ports_table(port_rows))

    if vulns:
        ui.section("VULNERABILITIES")
        ui.console.print(ui.vuln_table(vulns))

    # 7. Summary + save
    duration = time.time() - started
    total_open = sum(len(v) for v in port_results.values())
    ui.console.print()
    ui.console.print(ui.summary_panel(
        domain=domain, total=len(subdomains),
        live=len(live), dead=len(dead),
        takeover=len(takeover_findings),
        ports=total_open, vulns=len(vulns),
        duration=duration,
    ))
    ui.console.print()

    try:
        paths = save_reports(
            output_dir=output_dir, domain=domain,
            subdomains=subdomains, live=live, dead=dead,
            takeover=takeover_findings, ports=port_results,
            vulns=vulns, duration=duration,
        )
        ui.success(f"Reports saved to {paths['dir']}")
    except Exception as e:
        ui.error(f"Failed to save reports: {e}")


# ─────────────────────────────────────────────────────────────────────
# IP mode
# ─────────────────────────────────────────────────────────────────────

async def _run_ip_mode(
    ip: str,
    started: float,
    output_dir,
    ports: str,
    timeout: int,
    skip_ports: bool,
    skip_vuln: bool,
    skip_geo: bool,
    port_workers: int,
    nuclei_severity: str,
    probe_all_async,
    scan_ports_concurrently,
    scan_vulnerabilities,
    save_reports,
) -> None:

    # 1. Probe the IP as a single "host"
    ui.section("PHASE 1 — LIVENESS PROBING")
    results = await probe_all_async(
        [ip], concurrency=1, timeout=timeout, enrich_geo=not skip_geo,
    )
    live = [r for r in results if r["alive"]]
    dead = [r for r in results if not r["alive"]]
    ui.success(f"Live: {len(live)}  |  Dead: {len(dead)}")

    # 2. Ports
    port_results = {}
    if not skip_ports:
        ui.section("PHASE 2 — PORT SCANNING")
        port_results = scan_ports_concurrently(
            [ip], ports=ports, max_workers=port_workers,
        )
        total_open = sum(len(v) for v in port_results.values())
        ui.success(f"Open ports: {total_open}")

    # 3. Vulns (only if it responded to HTTP)
    vulns = []
    if not skip_vuln and live:
        ui.section("PHASE 3 — VULNERABILITY SCANNING")
        vulns = scan_vulnerabilities(live, severity=nuclei_severity)
        ui.success(f"Findings: {len(vulns)}")

    # 4. Tables
    ui.section("LIVE HOSTS")
    ui.console.print(ui.live_table(live))

    if dead:
        ui.section("DEAD HOSTS")
        ui.console.print(ui.dead_table(dead))

    if port_results:
        port_rows = [{"host": h, "ports": p}
                     for h, p in port_results.items() if p]
        if port_rows:
            ui.section("OPEN PORTS")
            ui.console.print(ui.ports_table(port_rows))

    if vulns:
        ui.section("VULNERABILITIES")
        ui.console.print(ui.vuln_table(vulns))

    # 5. Summary
    duration = time.time() - started
    total_open = sum(len(v) for v in port_results.values())
    ui.console.print()
    ui.console.print(ui.summary_panel(
        domain=ip, total=1,
        live=len(live), dead=len(dead),
        takeover=0, ports=total_open, vulns=len(vulns),
        duration=duration,
    ))
    ui.console.print()

    try:
        paths = save_reports(
            output_dir=output_dir, domain=ip,
            subdomains=[ip], live=live, dead=dead,
            takeover=[], ports=port_results,
            vulns=vulns, duration=duration,
        )
        ui.success(f"Reports saved to {paths['dir']}")
    except Exception as e:
        ui.error(f"Failed to save reports: {e}")


if __name__ == "__main__":
    app()