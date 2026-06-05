#!/usr/bin/env python3

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.align import Align
from rich import box
from rich.prompt import Prompt, Confirm
from collections import Counter
from ..utils.helpers import count_data_points

console = Console()


class TerminalUI:
    """Terminal UI for displaying investigation results"""
    
    @staticmethod
    def show_banner():
        """Display ASCII banner"""
        banner = """
╔════════════════════════════════════════════════════════════════════════╗
║   ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██████╗ ██╗   ██╗██╗     ║
║   ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║██╔══██╗██║   ██║██║     ║
║   ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║██████╔╝██║   ██║██║     ║
║   ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║██╔═══╝ ██║   ██║██║     ║
║   ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██║     ╚██████╔╝███████║
║   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝      ╚═════╝ ╚══════╝║
║                    Enterprise Email Intelligence Platform              ║
╚════════════════════════════════════════════════════════════════════════╝
        """
        console.print(banner, style="bold cyan")
        console.print("[bold yellow]Version 2.0.0[/] | [dim]IntelBase OSINT Platform[/]\n")
    
    @staticmethod
    def show_dashboard(data, email, risk_score, risk_level, risk_color, risk_icon):
        """Display main investigation dashboard"""
        meta = data.get('meta', {})
        breaches = data.get('data_breaches', {})
        accounts = data.get('identifier', {}).get('accounts', [])
        validator = data.get('validator', {})
        stealer = data.get('stealer_logs', {})
        
        console.print("\n")
        console.rule("[bold cyan] INTELLIGENCE REPORT [/]")
        
        # Target info panel
        target_info = (
            f"[bold white]Target:[/] [cyan]{email}[/]\n"
            f"[bold white]First Seen:[/] [green]{meta.get('first_seen', 'N/A')[:10]}[/]  "
            f"[bold white]Last Seen:[/] [yellow]{meta.get('last_seen', 'N/A')[:10]}[/]  "
            f"[bold white]Data Points:[/] [cyan]{count_data_points(data)}[/]"
        )
        console.print(Panel(
            target_info,
            title=f"[bold yellow]{risk_icon} Target Profile[/]",
            border_style="yellow"
        ))
        
        # Summary statistics table
        stats_table = Table(
            box=box.HEAVY,
            show_header=True,
            header_style="bold magenta",
            expand=True
        )
        
        stats_table.add_column("📊 Risk Score", justify="center", style=f"bold {risk_color}")
        stats_table.add_column("🔒 Breaches", justify="center", style="red")
        stats_table.add_column("👤 Accounts", justify="center", style="cyan")
        stats_table.add_column("✅ Registered", justify="center", style="green")
        stats_table.add_column("❌ Not Registered", justify="center", style="dim")
        stats_table.add_column("🦠 Stealer Logs", justify="center", style="yellow")
        
        breach_count = breaches.get('amount', 0)
        breach_sources = breaches.get('sources', 0)
        registered_count = len(validator.get('registered', []))
        unregistered_count = len(validator.get('unregistered', []))
        stealer_count = stealer.get('count', 0)
        
        stats_table.add_row(
            f"{risk_score}/100 [{risk_level}]",
            f"{breach_count}\nfrom {breach_sources} sources",
            str(len(accounts)),
            str(registered_count),
            str(unregistered_count),
            str(stealer_count)
        )
        
        console.print(stats_table)
    
    @staticmethod
    def show_accounts(data):
        """Display discovered accounts and profiles"""
        accounts = data.get('identifier', {}).get('accounts', [])
        
        if not accounts:
            console.print("[dim]No accounts discovered[/]")
            return
        
        console.print(f"\n[bold cyan]👤 DISCOVERED ACCOUNTS[/] [dim]({len(accounts)} total)[/]\n")
        
        for idx, acc in enumerate(accounts, 1):
            module = acc.get('module', {})
            acc_data = acc.get('data', {})
            service_name = module.get('name_formatted', 'Unknown')
            
            # Create account details table
            acc_table = Table(
                box=box.SIMPLE,
                show_header=False,
                title=f"[bold green]#{idx} - {service_name}[/]"
            )
            acc_table.add_column("Field", style="dim cyan", width=22)
            acc_table.add_column("Value", style="white")
            
            # List priority fields first
            priority_fields = [
                'username', 'user_id', 'id', 'full_name', 'display_name',
                'creation_date', 'last_login_date', 'profile_url', 'location',
                'followers', 'following', 'premium_status', 'is_verified',
                'country', 'bio', 'gender', 'birthday'
            ]
            
            for field in priority_fields:
                if field in acc_data and acc_data[field]:
                    val_str = str(acc_data[field])
                    # Truncate long values
                    if len(val_str) > 80:
                        val_str = val_str[:77] + "..."
                    acc_table.add_row(field, val_str)
            
            # Add other fields
            skip_fields = set(priority_fields + ['avatar_url', 'mx_hosts', 'google_stats'])
            for key, value in acc_data.items():
                if key not in skip_fields:
                    if value and value != [] and isinstance(value, (str, int, float, bool)):
                        acc_table.add_row(key, str(value)[:100])
            
            console.print(Panel(acc_table, border_style="green"))
    
    @staticmethod
    def show_breaches(data, current_email):
        """Display data breach information"""
        breaches = data.get('data_breaches', {})
        breach_results = breaches.get('results', [])
        
        if not breach_results:
            console.print("\n[green]✅ No breaches found![/]")
            return
        
        total = breaches.get('amount', 0)
        sources = breaches.get('sources', 0)
        console.print(f"\n[bold red]🔓 DATA BREACHES[/] [dim]({total} total from {sources} sources)[/]\n")
        
        # Extract passwords for analysis
        passwords = [b.get('password', '') for b in breach_results if b.get('password')]
        weak_passwords = [p for p in passwords if len(p) < 8]
        
        # Breach statistics
        stats_tbl = Table(box=box.SIMPLE, title="[bold]Breach Statistics[/]", title_style="bold red")
        stats_tbl.add_column("Metric", style="bold white")
        stats_tbl.add_column("Value", style="bold red")
        stats_tbl.add_row("Total Breaches", str(total))
        stats_tbl.add_row("Unique Sources", str(sources))
        stats_tbl.add_row("Passwords Exposed", str(len(passwords)))
        stats_tbl.add_row("Unique Passwords", str(len(set(passwords))))
        stats_tbl.add_row("Weak Passwords (<8 chars)", str(len(weak_passwords)))
        
        console.print(Panel(stats_tbl, border_style="red"))
        
        # Source breakdown
        source_counts = Counter()
        for breach in breach_results:
            src_name = breach.get('source', {}).get('name', 'Unknown')
            source_counts[src_name] += 1
        
        console.print("\n[bold yellow]Top Breach Sources:[/]")
        for src, count in source_counts.most_common(10):
            bar_chars = "█" * min(count, 40)
            console.print(f"  [cyan]{src}[/]: [red]{count}[/] {bar_chars}")
        
        # Show individual breaches
        console.print(f"\n[bold]Breach Details (showing first {min(30, len(breach_results))})[/]\n")
        for idx, breach in enumerate(breach_results[:30], 1):
            source = breach.get('source', {})
            info_parts = []
            
            info_parts.append(f"[cyan]Source:[/] {source.get('name', 'Unknown')}")
            
            if source.get('date'):
                info_parts.append(f"[yellow]Date:[/] {source['date']}")
            
            if breach.get('password'):
                pwd = breach['password']
                masked = f"{pwd[:2]}{'*' * (len(pwd)-2)}"
                info_parts.append(f"[red]Password:[/] [bold red]{masked}[/]")
            
            if breach.get('username'):
                info_parts.append(f"[dim]Username:[/] {breach['username']}")
            
            if breach.get('full_name'):
                info_parts.append(f"[dim]Name:[/] {breach['full_name']}")
            
            if breach.get('ip_address'):
                info_parts.append(f"[dim]IP:[/] {breach['ip_address']}")
            
            if breach.get('phone_number'):
                info_parts.append(f"[dim]Phone:[/] {breach['phone_number']}")
            
            if breach.get('email') and breach['email'] != current_email:
                info_parts.append(f"[dim]Alt Email:[/] {breach['email']}")
            
            console.print(Panel("\n".join(info_parts), title=f"[bold red]#{idx}[/]", border_style="red"))
    
    @staticmethod
    def show_registration(data):
        """Display registration status across platforms"""
        validator = data.get('validator', {})
        registered = validator.get('registered', [])
        unregistered = validator.get('unregistered', [])
        
        console.print(f"\n[bold green]✅ REGISTERED ({len(registered)})[/]")
        if registered:
            reg_text = Text()
            for svc in registered:
                svc_name = svc.get('name_formatted', 'Unknown')
                reg_text.append(f" {svc_name} ", style="bold white on dark_green")
                reg_text.append(" ")
            console.print(reg_text)
        else:
            console.print("[dim]None[/]")
        
        console.print(f"\n[bold red]❌ NOT REGISTERED ({len(unregistered)})[/]")
        if unregistered:
            unreg_text = Text()
            for svc in unregistered:
                svc_name = svc.get('name_formatted', 'Unknown')
                unreg_text.append(f" {svc_name} ", style="dim white on grey23")
                unreg_text.append(" ")
            console.print(unreg_text)
        else:
            console.print("[dim]None[/]")
    
    @staticmethod
    def show_stealer_logs(data):
        """Display stealer malware log information"""
        stealer = data.get('stealer_logs', {})
        count = stealer.get('count', 0)
        
        if count > 0:
            console.print(f"\n[bold magenta]🦠 STEALER LOGS: [red]{count}[/] found[/]")
            console.print("[red]⚠️  CRITICAL: Malware infection detected on this account![/]")
        else:
            console.print(f"\n[green]✅ No stealer logs detected[/]")
    
    @staticmethod
    def show_timeline(data):
        """Display activity timeline"""
        timeline = data.get('meta', {}).get('timeline', [])
        if not timeline:
            return
        
        console.print(f"\n[bold magenta]📅 TIMELINE ({len(timeline)} events)[/]\n")
        
        tbl = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold magenta")
        tbl.add_column("#", style="dim", width=4)
        tbl.add_column("Date", style="cyan", width=12)
        tbl.add_column("Platform", style="white")
        tbl.add_column("Event", style="dim")
        
        for idx, event in enumerate(timeline[:20], 1):
            event_date = event.get('date', '')[:10]
            platform = event.get('name', 'Unknown')
            event_type = event.get('source', 'Unknown')
            
            # Color code events
            if 'breach' in event_type.lower():
                event_style = "red"
            elif 'creation' in event_type.lower():
                event_style = "green"
            else:
                event_style = "dim"
            
            tbl.add_row(str(idx), event_date, platform, f"[{event_style}]{event_type}[/]")
        
        console.print(Panel(tbl, border_style="magenta"))
    
    @staticmethod
    def show_menu():
        """Display interactive menu"""
        console.print("\n[bold cyan]📋 MAIN MENU[/]")
        console.print("[1] [green]🔍 Single Investigation[/]")
        console.print("[2] [yellow]📊 Batch Investigation[/]")
        console.print("[3] [cyan]💾 Export Results[/]")
        console.print("[4] [magenta]📄 Generate HTML Report[/]")
        console.print("[5] [blue]📈 Show Statistics[/]")
        console.print("[6] [red]🚪 Exit[/]")
        
        choice = Prompt.ask("\n[bold]Select option[/]", choices=["1", "2", "3", "4", "5", "6"])
        return choice
