"""
S0NAR — terminal UI layer.

Everything that touches the screen lives here: the banner, the boot
sequence, the color theme, and every table the tool renders.

Author: LordXapose
Repo:   https://github.com/LordXapose/s0nar
"""

from __future__ import annotations

import time
from typing import Iterable

from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn, MofNCompleteColumn, Progress, SpinnerColumn,
    TextColumn, TimeElapsedColumn, TimeRemainingColumn,
)
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

THEME = Theme({
    "info":     "cyan",
    "success":  "bold green",
    "warning":  "bold yellow",
    "error":    "bold red",
    "muted":    "dim white",
    "url":      "underline cyan",
    "host":     "bold white",
    "port":     "magenta",
    "vuln":     "bold red",
    "takeover": "bold magenta",
    "brand":    "bold magenta",
    "brand2":   "bold cyan",
})

console = Console(theme=THEME)


def configure(no_color: bool = False, quiet: bool = False) -> None:
    global console
    console = Console(theme=THEME, no_color=no_color, quiet=quiet)


BANNER_ART = r"""
███████╗ ██████╗ ███╗   ██╗ █████╗ ██████╗
██╔════╝██╔═████╗████╗  ██║██╔══██╗██╔══██╗
███████╗██║██╔██║██╔██╗ ██║███████║██████╔╝
╚════██║████╔╝██║██║╚██╗██║██╔══██║██╔══██╗
███████║╚██████╔╝██║ ╚████║██║  ██║██║  ██║
╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝
"""

VERSION = "1.0.0"
AUTHOR = "LordXapose"
REPO = "github.com/LordXapose/s0nar"


def show_banner() -> None:
    console.print()
    console.print(Align.center(Text(BANNER_ART.strip("\n"), style="brand2")))
    console.print(Align.center(Text(f"── v{VERSION} ──", style="dim magenta")))
    console.print()
    console.print(Align.center(
        Text("▓▓ full-spectrum subdomain reconnaissance ▓▓", style="brand")
    ))
    console.print(Align.center(
        Text("ping the dark · hear what answers", style="italic dim cyan")
    ))
    console.print()

    credits = Text()
    credits.append("  dev   ", style="dim")
    credits.append(AUTHOR, style="bold cyan")
    credits.append("\n  repo  ", style="dim")
    credits.append(REPO, style="underline bright_cyan")
    credits.append("\n  lic   ", style="dim")
    credits.append("MIT", style="bold white")

    console.print(Align.center(Panel(
        credits, border_style="cyan", box=box.ROUNDED, padding=(0, 2),
    )))
    console.print()


def boot_sequence(backends: dict | None = None) -> None:
    if backends is None:
        backends = {}

    lines = [
        ("initializing s0nar engine...", "dim", 0.05),
        ("loading fingerprint database...", "dim", 0.05),
        ("  ↳ 63 services loaded", "green", 0.05),
        ("loading dns resolver pool...", "dim", 0.05),
        ("  ↳ 8.8.8.8 · 1.1.1.1 · 9.9.9.9", "green", 0.05),
        ("loading nmap service definitions...", "dim", 0.05),
        ("  ↳ 14,000+ signatures ready", "green", 0.05),
        ("checking subfinder / amass / nuclei...", "dim", 0.05),
    ]

    for msg, style, delay in lines:
        console.print(f"  [{style}]▸ {msg}[/]")
        time.sleep(delay)

    parts = []
    for name in ("subfinder", "amass", "nuclei", "nmap"):
        online = backends.get(name, True)
        mark = "●" if online else "○"
        color = "green" if online else "red"
        parts.append(Text(f" {mark} {name} ", style=color))

    console.print("  ↳", end=" ")
    console.print(*parts)
    console.print()
    console.print("  [bold red]▸ system armed.[/]")
    console.print()


def info(msg: str) -> None:
    console.print(f"[info]ℹ[/]  {msg}")


def success(msg: str) -> None:
    console.print(f"[success]✔[/]  {msg}")


def warn(msg: str) -> None:
    console.print(f"[warning]⚠[/]  {msg}")


def error(msg: str) -> None:
    console.print(f"[error]✘[/]  {msg}")


def section(title: str) -> None:
    console.print()
    console.print(Rule(f"[bold cyan]{title}[/]", style="cyan"))


def make_progress(label: str) -> Progress:
    return Progress(
        SpinnerColumn(style="cyan"),
        TextColumn(f"[bold cyan]{label}"),
        BarColumn(bar_width=None, complete_style="green", finished_style="green"),
        MofNCompleteColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=False,
    )


def _status_style(code):
    if code is None:
        return "DEAD", "error"
    if 200 <= code < 300:
        return str(code), "success"
    if 300 <= code < 400:
        return str(code), "info"
    if 400 <= code < 500:
        return str(code), "warning"
    return str(code), "error"


def _dot(code):
    if code is None:
        return "[red]●[/]"
    if 200 <= code < 300:
        return "[green]●[/]"
    if 300 <= code < 400:
        return "[cyan]●[/]"
    return "[yellow]●[/]"


def live_table(rows: Iterable[dict]) -> Table:
    rows = list(rows)
    table = Table(
        title=f"[bold green]LIVE SUBDOMAINS ({len(rows)})[/]",
        box=box.ROUNDED, header_style="bold green",
        border_style="green", expand=True, show_lines=False,
    )
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Host", style="host", overflow="fold")
    table.add_column("IP", style="cyan", overflow="fold")
    table.add_column("Status", justify="center", width=8)
    table.add_column("Server", style="muted", overflow="fold")
    table.add_column("Title", style="white", overflow="fold")

    for i, r in enumerate(rows, 1):
        code_text, code_style = _status_style(r.get("status_code"))
        table.add_row(
            str(i),
            f"{_dot(r.get('status_code'))} {r['host']}",
            r.get("ip") or "-",
            f"[{code_style}]{code_text}[/]",
            (r.get("server") or "-")[:30],
            (r.get("title") or "-")[:40],
        )
    return table


def dead_table(rows: Iterable[dict]) -> Table:
    rows = list(rows)
    table = Table(
        title=f"[bold red]CLOSED / DEAD SUBDOMAINS ({len(rows)})[/]",
        box=box.ROUNDED, header_style="bold red",
        border_style="red", expand=True,
    )
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Host", style="host", overflow="fold")
    table.add_column("IP", style="cyan", overflow="fold")
    table.add_column("Reason", style="muted")

    for i, r in enumerate(rows, 1):
        table.add_row(
            str(i),
            f"[red]●[/] {r['host']}",
            r.get("ip") or "-",
            r.get("reason") or "no HTTP/HTTPS response",
        )
    return table


def takeover_table(rows: Iterable[dict]) -> Table:
    rows = list(rows)
    table = Table(
        title=f"[bold magenta]SUBDOMAIN TAKEOVER CANDIDATES ({len(rows)})[/]",
        box=box.ROUNDED, header_style="bold magenta",
        border_style="magenta", expand=True,
    )
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Host", style="host", overflow="fold")
    table.add_column("CNAME", style="cyan", overflow="fold")
    table.add_column("Service", style="magenta")
    table.add_column("Confidence", justify="center", width=12)

    conf_styles = {
        "confirmed": "bold red",
        "cname-only": "bold yellow",
        "dangling": "bold magenta",
    }
    for i, r in enumerate(rows, 1):
        style = conf_styles.get(r.get("confidence", ""), "white")
        table.add_row(
            str(i),
            f"[magenta]●[/] {r['host']}",
            r.get("cname", "-"),
            r.get("service", "-"),
            f"[{style}]{r.get('confidence', '-').upper()}[/]",
        )
    return table


def ports_table(rows: Iterable[dict]) -> Table:
    rows = list(rows)
    table = Table(
        title=f"[bold cyan]OPEN PORTS & SERVICES ({len(rows)} hosts)[/]",
        box=box.ROUNDED, header_style="bold cyan",
        border_style="cyan", expand=True,
    )
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Host", style="host", overflow="fold")
    table.add_column("Services", style="white", overflow="fold")

    for i, r in enumerate(rows, 1):
        bits = []
        for p in r.get("ports", []):
            port = p.get("port")
            svc = p.get("service", "") or "unknown"
            prod = " ".join(filter(None, [
                p.get("product", ""), p.get("version", ""),
            ]))
            label = f"[port]{port}[/]/[cyan]{svc}[/]"
            if prod:
                label += f" [dim]{prod}[/]"
            bits.append(label)
        table.add_row(
            str(i), r["host"],
            " · ".join(bits) if bits else "[dim]none[/]",
        )
    return table


def vuln_table(rows: Iterable[dict]) -> Table:
    rows = list(rows)
    table = Table(
        title=f"[bold red]VULNERABILITIES ({len(rows)})[/]",
        box=box.ROUNDED, header_style="bold red",
        border_style="red", expand=True,
    )
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Severity", justify="center", width=10)
    table.add_column("URL", style="url", overflow="fold")
    table.add_column("Finding", style="white", overflow="fold")

    sev_styles = {
        "critical": "bold white on red",
        "high": "bold red",
        "medium": "bold yellow",
        "low": "cyan",
        "info": "dim",
    }
    for i, v in enumerate(rows, 1):
        info_d = v.get("info", {}) if isinstance(v.get("info"), dict) else {}
        sev = (v.get("severity") or info_d.get("severity") or "info").lower()
        sev_style = sev_styles.get(sev, "white")
        name = v.get("name") or info_d.get("name") or v.get("type", "-")
        url = v.get("url") or v.get("matched-at") or v.get("host", "-")
        table.add_row(
            str(i),
            f"[{sev_style}]{sev.upper()}[/]",
            url, name,
        )
    return table


def summary_panel(domain, total, live, dead, takeover, ports, vulns, duration) -> Panel:
    grid = Table.grid(padding=(0, 2))
    grid.add_column(justify="right", style="bold white")
    grid.add_column(justify="left", style="bold cyan")

    grid.add_row("Target:", f"[cyan]{domain}[/]")
    grid.add_row("Duration:", f"[cyan]{duration:.1f}s[/]")
    grid.add_row("", "")
    grid.add_row("Total discovered:", str(total))
    grid.add_row("[green]Live hosts:[/]", f"[green]{live}[/]")
    grid.add_row("[red]Dead hosts:[/]", f"[red]{dead}[/]")
    grid.add_row("[magenta]Takeover candidates:[/]", f"[magenta]{takeover}[/]")
    grid.add_row("[cyan]Open ports:[/]", f"[cyan]{ports}[/]")
    grid.add_row("[red]Vulnerabilities:[/]", f"[red]{vulns}[/]")

    return Panel(
        Align.center(grid),
        title="[bold cyan]SCAN SUMMARY[/]",
        border_style="cyan", box=box.DOUBLE, padding=(1, 4),
    )


if __name__ == "__main__":
    show_banner()
    boot_sequence({"subfinder": True, "amass": True, "nuclei": True, "nmap": False})
    section("LIVE SUBDOMAINS")
    console.print(live_table([
        {"host": "api.example.com", "ip": "104.18.32.47",
         "status_code": 200, "server": "nginx/1.18", "title": "API Home"},
    ]))