#!/usr/bin/env python3

import sys
from pathlib import Path
from rich.prompt import Prompt, Confirm
from rich.rule import Rule
from rich.console import Console

from .core.engine import ReconEngine
from .display.terminal_ui import TerminalUI
from .export.exporter import Exporter

console = Console()
ui = TerminalUI()
engine = ReconEngine()
exporter = Exporter()


def single_investigation():
    """Run a single email investigation"""
    email = Prompt.ask("[bold cyan]Enter target email[/]")
    
    # Validate email format
    if not email or '@' not in email:
        console.print("[red]Invalid email format![/]")
        return
    
    try:
        data = engine.investigate(email)
    except Exception as e:
        console.print(f"[red]Investigation failed: {str(e)}[/]")
        return
    
    # Calculate risk metrics
    risk_score = engine.calculate_risk(data)
    risk_level, risk_color, risk_icon = engine.get_risk_level(risk_score)
    
    # Display results
    ui.show_dashboard(data, email, risk_score, risk_level, risk_color, risk_icon)
    ui.show_accounts(data)
    ui.show_breaches(data, email)
    ui.show_stealer_logs(data)
    ui.show_registration(data)
    ui.show_timeline(data)
    
    console.print(Rule("[dim]Investigation Complete[/]", style="dim"))
    
    # Prompt for export
    if Confirm.ask("\n[yellow]Export results?[/]", default=True):
        fmt = Prompt.ask("[cyan]Choose format[/]", choices=["json", "csv", "html"], default="json")
        try:
            filename = exporter.export(data, email, fmt)
            console.print(f"[green]✅ Results saved: {filename}[/]")
        except Exception as e:
            console.print(f"[red]Export error: {e}[/]")


def batch_investigation():
    """Process multiple emails from a file"""
    filepath = Prompt.ask("[cyan]Path to email list file[/]")
    
    if not Path(filepath).exists():
        console.print("[red]File not found[/]")
        return
    
    # Load emails from file
    try:
        with open(filepath, 'r') as f:
            emails = [line.strip() for line in f if line.strip() and '@' in line]
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/]")
        return
    
    if not emails:
        console.print("[yellow]No valid emails found in file[/]")
        return
    
    console.print(f"\n[cyan]Processing {len(emails)} emails...\n[/]")
    
    # Process each email
    for idx, email in enumerate(emails, 1):
        console.print(f"[{idx}/{len(emails)}] {email}...", end=" ", flush=True)
        try:
            data = engine.investigate(email)
            risk = engine.calculate_risk(data)
            breaches = data.get('data_breaches', {}).get('amount', 0)
            console.print(f"[green]✓ Risk: {risk}/100 | Breaches: {breaches}[/]")
        except Exception as e:
            console.print(f"[red]✗ Failed: {str(e)[:40]}[/]")


def export_results():
    """Export previously saved results"""
    if not engine.current_data:
        console.print("[red]No investigation data to export[/]")
        return
    
    fmt = Prompt.ask("[cyan]Format[/]", choices=["json", "csv", "html"], default="json")
    email = engine.current_email or "unknown"
    
    try:
        filename = exporter.export(engine.current_data, email, fmt)
        console.print(f"[green]✅ Exported: {filename}[/]")
    except Exception as e:
        console.print(f"[red]Export failed: {e}[/]")


def html_report():
    """Generate HTML report for an email"""
    email = Prompt.ask("[cyan]Email address[/]")
    
    try:
        console.print("[cyan]Generating report...[/]")
        data = engine.investigate(email)
        filename = exporter.export(data, email, 'html')
        console.print(f"[green]✅ Report saved: {filename}[/]")
    except Exception as e:
        console.print(f"[red]Report generation failed: {e}[/]")


def show_stats():
    """Display statistics from current investigation"""
    if not engine.current_data:
        console.print("[yellow]⚠️  No data available. Run an investigation first.[/]")
        return
    
    from .utils.helpers import count_data_points
    
    data = engine.current_data
    total_points = count_data_points(data)
    num_accounts = len(data.get('identifier', {}).get('accounts', []))
    num_breaches = data.get('data_breaches', {}).get('amount', 0)
    risk = engine.calculate_risk(data)
    
    console.print("\n[bold cyan]📊 Investigation Statistics[/]")
    console.print(f"  Total Data Points: {total_points}")
    console.print(f"  Discovered Accounts: {num_accounts}")
    console.print(f"  Breach Count: {num_breaches}")
    console.print(f"  Overall Risk: {risk}/100")


def main():
    """Main CLI entry point"""
    ui.show_banner()
    
    # Handle command-line arguments
    if len(sys.argv) > 1:
        email_arg = sys.argv[1]
        
        try:
            data = engine.investigate(email_arg)
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
            return
        
        risk_score = engine.calculate_risk(data)
        risk_level, risk_color, risk_icon = engine.get_risk_level(risk_score)
        
        ui.show_dashboard(data, email_arg, risk_score, risk_level, risk_color, risk_icon)
        ui.show_accounts(data)
        ui.show_breaches(data, email_arg)
        ui.show_stealer_logs(data)
        ui.show_registration(data)
        ui.show_timeline(data)
        
        # Export if format specified
        if len(sys.argv) > 2:
            fmt = sys.argv[2]
            try:
                filename = exporter.export(data, email_arg, fmt)
                console.print(f"\n[green]✅ Saved: {filename}[/]")
            except Exception as e:
                console.print(f"[red]Export failed: {e}[/]")
        
        return
    
    # Interactive menu mode
    while True:
        choice = ui.show_menu()
        
        if choice == "1":
            single_investigation()
        elif choice == "2":
            batch_investigation()
        elif choice == "3":
            export_results()
        elif choice == "4":
            html_report()
        elif choice == "5":
            show_stats()
        elif choice == "6":
            console.print("[yellow]Exiting...👋[/]")
            break


if __name__ == "__main__":
    main()
