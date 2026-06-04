"""
Professional Terminal UI
"""
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
    """Professional display interface"""
    
    @staticmethod
    def show_banner():
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║   ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██████╗ ██╗   ██╗██╗     ███████╗
║   ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║██╔══██╗██║   ██║██║     ██╔════╝
║   ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║██████╔╝██║   ██║██║     ███████╗
║   ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║██╔═══╝ ██║   ██║██║     ╚════██║
║   ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██║     ╚██████╔╝███████╗███████║
║   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝      ╚═════╝ ╚══════╝╚══════╝
║                    Advanced Email Intelligence Platform                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        console.print(banner, style="bold cyan")
        console.print("[bold yellow]Version 2.0.0 Enterprise[/] | [dim]Powered by IntelBase API[/]\n")
    
    @staticmethod
    def show_dashboard(data, email, risk_score, risk_level, risk_color, risk_icon):
        """Show executive dashboard"""
        meta = data.get('meta', {})
        breaches = data.get('data_breaches', {})
        accounts = data.get('identifier', {}).get('accounts', [])
        validator = data.get('validator', {})
        stealer = data.get('stealer_logs', {})
        
        console.print("\n")
        console.rule("[bold cyan] INTELLIGENCE REPORT [/]")
        
        console.print(Panel(
            f"[bold white]Target:[/] [cyan]{email}[/]\n"
            f"[bold white]First Seen:[/] [green]{meta.get('first_seen', 'N/A')[:10]}[/]  "
            f"[bold white]Last Seen:[/] [yellow]{meta.get('last_seen', 'N/A')[:10]}[/]  "
            f"[bold white]Data Points:[/] [cyan]{count_data_points(data)}[/]",
            title=f"[bold yellow]{risk_icon} Target Profile[/]",
            border_style="yellow"
        ))
        
        dashboard = Table(
            box=box.HEAVY,
            show_header=True,
            header_style="bold magenta",
            expand=True
        )
        
        dashboard.add_column(f"📊 Risk Score", justify="center", style=f"bold {risk_color}")
        dashboard.add_column("🔒 Breaches", justify="center", style="red")
        dashboard.add_column("👤 Accounts", justify="center", style="cyan")
        dashboard.add_column("✅ Registered", justify="center", style="green")
        dashboard.add_column("❌ Not Registered", justify="center", style="dim")
        dashboard.add_column("🦠 Stealer Logs", justify="center", style="yellow")
        
        dashboard.add_row(
            f"{risk_score}/100 [{risk_level}]",
            f"{breaches.get('amount', 0)}\nfrom {breaches.get('sources', 0)} sources",
            str(len(accounts)),
            str(len(validator.get('registered', []))),
            str(len(validator.get('unregistered', []))),
            str(stealer.get('count', 0))
        )
        
        console.print(dashboard)
    
    @staticmethod
    def show_accounts(data):
        """Show all accounts with details"""
        accounts = data.get('identifier', {}).get('accounts', [])
        
        if not accounts:
            console.print("[dim]No accounts discovered[/]")
            return
        
        console.print(f"\n[bold cyan]👤 DISCOVERED ACCOUNTS[/] [dim]({len(accounts)} total)[/]\n")
        
        for i, acc in enumerate(accounts, 1):
            module = acc.get('module', {})
            acc_data = acc.get('data', {})
            service_name = module.get('name_formatted', 'Unknown')
            
            acc_table = Table(
                box=box.SIMPLE,
                show_header=False,
                title=f"[bold green]#{i} - {service_name}[/]"
            )
            acc_table.add_column("Field", style="dim cyan", width=22)
            acc_table.add_column("Value", style="white")
            
            for field in ['username', 'user_id', 'id', 'full_name', 'display_name',
                         'creation_date', 'last_login_date', 'profile_url', 'location',
                         'followers', 'following', 'premium_status', 'is_verified',
                         'country', 'bio', 'gender', 'birthday']:
                if field in acc_data and acc_data[field]:
                    value = str(acc_data[field])
                    if len(value) > 80:
                        value = value[:77] + "..."
                    acc_table.add_row(field, value)
            
            for key, value in acc_data.items():
                if key not in ['username', 'user_id', 'id', 'full_name', 'display_name',
                              'creation_date', 'last_login_date', 'profile_url', 'location',
                              'followers', 'following', 'premium_status', 'is_verified',
                              'country', 'bio', 'gender', 'birthday', 'avatar_url', 'mx_hosts', 'google_stats']:
                    if value and value != [] and isinstance(value, (str, int, float, bool)):
                        acc_table.add_row(key, str(value)[:100])
            
            console.print(Panel(acc_table, border_style="green"))
    
    @staticmethod
    def show_breaches(data, current_email):
        """Show ALL breaches"""
        breaches = data.get('data_breaches', {})
        breach_results = breaches.get('results', [])
        
        if not breach_results:
            console.print("\n[green]✅ No breaches found![/]")
            return
        
        console.print(f"\n[bold red]🔓 DATA BREACHES[/] [dim]({breaches.get('amount', 0)} total from {breaches.get('sources', 0)} sources)[/]\n")
        
        passwords = [b.get('password', '') for b in breach_results if b.get('password')]
        
        stats_table = Table(box=box.SIMPLE, title="[bold]Breach Statistics[/]", title_style="bold red")
        stats_table.add_column("Metric", style="bold white")
        stats_table.add_column("Value", style="bold red")
        stats_table.add_row("Total Breaches", str(breaches.get('amount', 0)))
        stats_table.add_row("Unique Sources", str(breaches.get('sources', 0)))
        stats_table.add_row("Passwords Exposed", str(len(passwords)))
        stats_table.add_row("Unique Passwords", str(len(set(passwords))))
        stats_table.add_row("Weak Passwords (<8)", str(len([p for p in passwords if len(p) < 8])))
        
        console.print(Panel(stats_table, border_style="red"))
        
        # Source breakdown
        sources = Counter()
        for breach in breach_results:
            sources[breach.get('source', {}).get('name', 'Unknown')] += 1
        
        console.print("\n[bold yellow]Top Breach Sources:[/]")
        for source, count in sources.most_common(10):
            bar = "█" * min(count, 40)
            console.print(f"  [cyan]{source}[/]: [red]{count}[/] {bar}")
        
        # Show breaches
        console.print(f"\n[bold]Breach Details (first 30):[/]\n")
        for i, breach in enumerate(breach_results[:30], 1):
            source = breach.get('source', {})
            info = []
            info.append(f"[cyan]Source:[/] {source.get('name', 'Unknown')}")
            if source.get('date'):
                info.append(f"[yellow]Date:[/] {source['date']}")
            if breach.get('password'):
                pwd = breach['password']
                info.append(f"[red]Password:[/] [bold red]{pwd[:2]}{'*' * (len(pwd)-2)}[/]")
            if breach.get('username'):
                info.append(f"[dim]Username:[/] {breach['username']}")
            if breach.get('full_name'):
                info.append(f"[dim]Name:[/] {breach['full_name']}")
            if breach.get('ip_address'):
                info.append(f"[dim]IP:[/] {breach['ip_address']}")
            if breach.get('phone_number'):
                info.append(f"[dim]Phone:[/] {breach['phone_number']}")
            if breach.get('email') and breach['email'] != current_email:
                info.append(f"[dim]Alt Email:[/] {breach['email']}")
            
            console.print(Panel("\n".join(info), title=f"[bold red]#{i}[/]", border_style="red"))
    
    @staticmethod
    def show_registration(data):
        """Show registration status"""
        validator = data.get('validator', {})
        registered = validator.get('registered', [])
        unregistered = validator.get('unregistered', [])
        
        console.print(f"\n[bold green]✅ REGISTERED ({len(registered)})[/]")
        if registered:
            reg_text = Text()
            for s in registered:
                reg_text.append(f" {s.get('name_formatted', 'Unknown')} ", style="bold white on dark_green")
                reg_text.append(" ")
            console.print(reg_text)
        
        console.print(f"\n[bold red]❌ NOT REGISTERED ({len(unregistered)})[/]")
        if unregistered:
            unreg_text = Text()
            for s in unregistered:
                unreg_text.append(f" {s.get('name_formatted', 'Unknown')} ", style="dim white on grey23")
                unreg_text.append(" ")
            console.print(unreg_text)
    
    @staticmethod
    def show_stealer_logs(data):
        """Show stealer logs"""
        stealer = data.get('stealer_logs', {})
        count = stealer.get('count', 0)
        
        if count > 0:
            console.print(f"\n[bold magenta]🦠 STEALER LOGS: [red]{count}[/] found[/]")
            console.print("[red]⚠️ CRITICAL: Malware infection detected![/]")
        else:
            console.print(f"\n[green]✅ No stealer logs[/]")
    
    @staticmethod
    def show_timeline(data):
        """Show timeline"""
        timeline = data.get('meta', {}).get('timeline', [])
        if not timeline:
            return
        
        console.print(f"\n[bold magenta]📅 TIMELINE ({len(timeline)} events)[/]\n")
        
        table = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Date", style="cyan", width=12)
        table.add_column("Platform", style="white")
        table.add_column("Event", style="dim")
        
        for i, event in enumerate(timeline[:20], 1):
            date = event.get('date', '')[:10]
            platform = event.get('name', 'Unknown')
            event_type = event.get('source', 'Unknown')
            
            style = "red" if 'breach' in event_type.lower() else "green" if 'creation' in event_type.lower() else "dim"
            table.add_row(str(i), date, platform, f"[{style}]{event_type}[/]")
        
        console.print(Panel(table, border_style="magenta"))
    
    @staticmethod
    def show_menu():
        """Show main menu"""
        console.print("\n[bold cyan]📋 MAIN MENU[/]")
        console.print("[1] [green]🔍 Single Investigation[/]")
        console.print("[2] [yellow]📊 Batch Investigation[/]")
        console.print("[3] [cyan]💾 Export Results[/]")
        console.print("[4] [magenta]📄 HTML Report[/]")
        console.print("[5] [blue]📈 Statistics[/]")
        console.print("[6] [red]🚪 Exit[/]")
        return Prompt.ask("\n[bold]Select option[/]", choices=["1", "2", "3", "4", "5", "6"])
