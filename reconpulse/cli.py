#!/usr/bin/env python3
"""
ReconPulse CLI - Main interface
"""
import sys
from pathlib import Path
from rich.prompt import Prompt, Confirm

from .core.engine import ReconEngine
from .display.terminal_ui import TerminalUI
from .export.exporter import Exporter

ui = TerminalUI()
engine = ReconEngine()
exporter = Exporter()

def single_investigation():
    """Run single email investigation"""
    email = Prompt.ask("[bold cyan]Enter target email[/]")
    
    if not email or '@' not in email:
        ui.show_error = lambda msg: print(f"[red]{msg}[/]")
        print("[red]Invalid email![/]")
        return
    
    try:
        data = engine.investigate(email)
    except Exception as e:
        print(f"[red]Error: {e}[/]")
        return
    
    risk_score = engine.calculate_risk(data)
    risk_level, risk_color, risk_icon = engine.get_risk_level(risk_score)
    
    ui.show_dashboard(data, email, risk_score, risk_level, risk_color, risk_icon)
    ui.show_accounts(data)
    ui.show_breaches(data, email)
    ui.show_stealer_logs(data)
    ui.show_registration(data)
    ui.show_timeline(data)
    
    from rich.rule import Rule
    from rich.console import Console
    Console().print(Rule("[dim]Investigation Complete[/]"))
    
    if Confirm.ask("\n[yellow]Export results?[/]", default=True):
        fmt = Prompt.ask("[cyan]Format[/]", choices=["json", "csv", "html"], default="json")
        filename = exporter.export(data, email, fmt)
        print(f"[green]✅ Exported: {filename}[/]")

def batch_investigation():
    """Run batch investigation"""
    filepath = Prompt.ask("[cyan]Email list file[/]")
    
    if not Path(filepath).exists():
        print("[red]File not found![/]")
        return
    
    with open(filepath) as f:
        emails = [l.strip() for l in f if l.strip() and '@' in l]
    
    print(f"\n[cyan]Processing {len(emails)} emails...[/]\n")
    
    for i, email in enumerate(emails, 1):
        print(f"[{i}/{len(emails)}] {email}...", end=" ")
        try:
            data = engine.investigate(email)
            risk = engine.calculate_risk(data)
            breaches = data.get('data_breaches', {}).get('amount', 0)
            print(f"[green]✓ Risk: {risk}/100 | Breaches: {breaches}[/]")
        except Exception as e:
            print(f"[red]✗ {e}[/]")

def export_results():
    """Export current results"""
    if not engine.current_data:
        print("[red]No results to export![/]")
        return
    
    fmt = Prompt.ask("[cyan]Format[/]", choices=["json", "csv", "html"], default="json")
    filename = exporter.export(engine.current_data, engine.current_email or "unknown", fmt)
    print(f"[green]✅ Exported: {filename}[/]")

def html_report():
    """Generate HTML report"""
    email = Prompt.ask("[cyan]Enter email[/]")
    try:
        data = engine.investigate(email)
        filename = exporter.export(data, email, 'html')
        print(f"[green]✅ HTML report: {filename}[/]")
    except Exception as e:
        print(f"[red]Error: {e}[/]")

def show_stats():
    """Show statistics"""
    if not engine.current_data:
        print("[yellow]No data. Run investigation first.[/]")
        return
    
    from ..utils.helpers import count_data_points
    data = engine.current_data
    
    print(f"\n[bold cyan]📊 Statistics[/]")
    print(f"  Data Points: {count_data_points(data)}")
    print(f"  Accounts: {len(data.get('identifier', {}).get('accounts', []))}")
    print(f"  Breaches: {data.get('data_breaches', {}).get('amount', 0)}")
    print(f"  Risk Score: {engine.calculate_risk(data)}/100")

def main():
    """Main entry point"""
    ui.show_banner()
    
    # Command line mode
    if len(sys.argv) > 1:
        email = sys.argv[1]
        try:
            data = engine.investigate(email)
        except Exception as e:
            print(f"[red]Error: {e}[/]")
            return
        
        risk_score = engine.calculate_risk(data)
        risk_level, risk_color, risk_icon = engine.get_risk_level(risk_score)
        
        ui.show_dashboard(data, email, risk_score, risk_level, risk_color, risk_icon)
        ui.show_accounts(data)
        ui.show_breaches(data, email)
        ui.show_stealer_logs(data)
        ui.show_registration(data)
        ui.show_timeline(data)
        
        if len(sys.argv) > 2:
            filename = exporter.export(data, email, sys.argv[2])
            print(f"\n[green]✅ Exported: {filename}[/]")
        
        return
    
    # Interactive mode
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
            print("[yellow]👋 Goodbye![/]")
            break

if __name__ == "__main__":
    main()
