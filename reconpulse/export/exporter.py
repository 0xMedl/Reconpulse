"""
Export results in multiple formats
"""
import json
import csv
from pathlib import Path
from datetime import datetime
from ..utils.helpers import sanitize_filename, get_timestamp

class Exporter:
    """Handle all exports"""
    
    def __init__(self, output_dir="./results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def export(self, data, email, format='json'):
        """Export data in specified format"""
        timestamp = get_timestamp()
        safe_email = sanitize_filename(email)
        
        if format == 'json':
            return self._export_json(data, safe_email, timestamp)
        elif format == 'csv':
            return self._export_csv(data, safe_email, timestamp)
        elif format == 'html':
            return self._export_html(data, email, safe_email, timestamp)
    
    def _export_json(self, data, safe_email, timestamp):
        """Export as JSON"""
        filename = self.output_dir / f"recon_{safe_email}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        return str(filename)
    
    def _export_csv(self, data, safe_email, timestamp):
        """Export breaches as CSV"""
        filename = self.output_dir / f"recon_{safe_email}_{timestamp}.csv"
        breaches = data.get('data_breaches', {}).get('results', [])
        
        if breaches:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'source', 'date', 'email', 'password', 'username',
                    'full_name', 'ip_address', 'phone_number', 'hash'
                ])
                writer.writeheader()
                for b in breaches:
                    writer.writerow({
                        'source': b.get('source', {}).get('name', ''),
                        'date': b.get('source', {}).get('date', ''),
                        'email': b.get('email', ''),
                        'password': b.get('password', ''),
                        'username': b.get('username', ''),
                        'full_name': b.get('full_name', ''),
                        'ip_address': b.get('ip_address', ''),
                        'phone_number': b.get('phone_number', ''),
                        'hash': b.get('hash', '')
                    })
        
        return str(filename)
    
    def _export_html(self, data, email, safe_email, timestamp):
        """Generate HTML report"""
        filename = self.output_dir / f"recon_{safe_email}_{timestamp}.html"
        
        # Calculate risk
        risk = min(
            data.get('data_breaches', {}).get('amount', 0) * 2 +
            data.get('stealer_logs', {}).get('count', 0) * 5 +
            len(data.get('identifier', {}).get('accounts', [])),
            100
        )
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>ReconPulse Report - {email}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #0a0e27; color: #e0e0e0; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 30px; border-radius: 10px; }}
        .header h1 {{ color: white; }}
        .email {{ font-size: 24px; color: #ffd700; }}
        .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 20px 0; }}
        .card {{ background: #1a1f3a; padding: 20px; border-radius: 10px; text-align: center; }}
        .stat-value {{ font-size: 36px; font-weight: bold; color: #ffd700; }}
        .stat-label {{ color: #888; }}
        .breach {{ background: #2a0000; border-left: 3px solid #ff4444; padding: 10px; margin: 10px 0; }}
        .breach strong {{ color: #ff6666; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 ReconPulse Intelligence Report</h1>
        <div class="email">{email}</div>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    <div class="grid">
        <div class="card"><div class="stat-value">{risk}/100</div><div class="stat-label">Risk Score</div></div>
        <div class="card"><div class="stat-value">{data.get('data_breaches', {}).get('amount', 0)}</div><div class="stat-label">Breaches</div></div>
        <div class="card"><div class="stat-value">{len(data.get('identifier', {}).get('accounts', []))}</div><div class="stat-label">Accounts</div></div>
        <div class="card"><div class="stat-value">{data.get('stealer_logs', {}).get('count', 0)}</div><div class="stat-label">Stealer Logs</div></div>
    </div>
    <h2>Breach Details</h2>
"""
        
        for breach in data.get('data_breaches', {}).get('results', [])[:50]:
            source = breach.get('source', {})
            pwd = breach.get('password', '')
            html += f'<div class="breach"><strong>{source.get("name", "Unknown")}</strong><br>'
            if source.get('date'): html += f'Date: {source["date"]}<br>'
            if pwd: html += f'Password: {pwd[:2]}{"*" * (len(pwd)-2)}<br>'
            if breach.get('username'): html += f'Username: {breach["username"]}<br>'
            html += '</div>'
        
        html += '</body></html>'
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return str(filename)
