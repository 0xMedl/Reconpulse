"""
IntelBase API Client
"""
import requests
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.console import Console

console = Console()

class IntelBaseClient:
    """Handle all API communications"""
    
    def __init__(self, api_key, base_url="https://api.intelbase.is"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": api_key,
            "Content-Type": "application/json"
        })
    
    def lookup_email(self, email, timeout_ms=60000):
        """Lookup email with ALL data"""
        url = f"{self.base_url}/lookup/email"
        
        payload = {
            "email": email,
            "timeout_ms": timeout_ms,
            "include_data_breaches": True,
            "exclude_modules": []
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Extracting intelligence data...", total=100)
            
            try:
                response = self.session.post(url, json=payload, timeout=60)
                progress.update(task, advance=50)
                
                if response.status_code == 200:
                    data = response.json()
                    progress.update(task, advance=50)
                    return {"success": True, "data": data}
                else:
                    return {"success": False, "error": f"API Error {response.status_code}"}
                    
            except Exception as e:
                return {"success": False, "error": str(e)}
