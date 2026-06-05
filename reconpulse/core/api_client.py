#!/usr/bin/env python3

import requests
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.console import Console

console = Console()


class IntelBaseClient:
    """Handles communication with IntelBase API"""
    
    def __init__(self, api_key, base_url="https://api.intelbase.is"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": api_key,
            "Content-Type": "application/json"
        })
    
    def lookup_email(self, email, timeout_ms=60000):
        """Perform email lookup with full data extraction"""
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
            task = progress.add_task("[cyan]Extracting intelligence...", total=100)
            
            try:
                resp = self.session.post(url, json=payload, timeout=60)
                progress.update(task, advance=50)
                
                if resp.status_code == 200:
                    result_data = resp.json()
                    progress.update(task, advance=50)
                    return {"success": True, "data": result_data}
                else:
                    err_msg = f"API returned status {resp.status_code}"
                    return {"success": False, "error": err_msg}
                    
            except requests.exceptions.Timeout:
                return {"success": False, "error": "Request timed out"}
            except requests.exceptions.ConnectionError:
                return {"success": False, "error": "Connection error"}
            except Exception as e:
                return {"success": False, "error": f"Error: {str(e)}"}
