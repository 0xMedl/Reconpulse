#!/usr/bin/env python3

import json
import csv
from pathlib import Path
from datetime import datetime
from ..utils.helpers import sanitize_filename, get_timestamp


class Exporter:
    """Export investigation results in various formats"""
    
    def __init__(self, output_dir="./results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def export(self, data, email, format='json'):
        """Export data in specified format (json, csv, html)"""
        if not format in ['json', 'csv', 'html']:
            raise ValueError(f"Unsupported format: {format}")
        
        timestamp = get_timestamp()
        safe_email = sanitize_filename(email)
        
        if format == 'json':
            return self._export_json(data, safe_email, timestamp)
        elif format == 'csv':
            return self._export_csv(data, safe_email, timestamp)
        elif format == 'html':
            return self._export_html(data, email, safe_email, timestamp)
    
    def _export_json(self, data, safe_email, timestamp):
        """Export full data as JSON"""
        filename = self.output_dir / f"recon_{safe_email}_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            return str(filename)
        except Exception as e:
            raise Exception(f"Failed to write JSON: {e}")
    
    def _export_csv(self, data, safe_email, timestamp):
        """Export breach data as CSV"""
        filename = self.output_dir / f"recon_{safe_email}_{timestamp}.csv"
        breaches = data.get('data_breaches', {}).get('results', [])
        
        if not breaches:
            return str(filename)
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'source', 'date', 'email', 'password', 'username',
                    'full_name', 'ip_address', 'phone_number', 'hash'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for breach in breaches:
                    source_info = breach.get('source', {})
                    row = {
                        'source': source_info.get('name', ''),
                        'date': source_info.get('date', ''),
                        'email': breach.get('email', ''),
                        'password': breach.get('password', ''),
                        'username': breach.get('username', ''),
                        'full_name': breach.get('full_name', ''),
                        'ip_address': breach.get('ip_address', ''),
                        'phone_number': breach.get('phone_number', ''),
                        'hash': breach.get('hash', '')
                    }
                    writer.writerow(row)
        
        except Exception as e:
            raise Exception(f"Failed to write CSV: {e}")
        
        return str(filename)
    
    def _export_html(self, data, email, safe_email, timestamp):
        """Generate professional HTML report"""
        filename = self.output_dir / f"recon_{safe_email}_{timestamp}.html"
        
        # Calculate metrics
        risk = min(
            data.get('data_breaches', {}).get('amount', 0) * 2 +
            data.get('stealer_logs', {}).get('count', 0) * 5 +
            len(data.get('identifier', {}).get('accounts', [])),
            100
        )
        
        breach_count = data.get('data_breaches', {}).get('amount', 0)
        account_count = len(data.get('identifier', {}).get('accounts', []))
        stealer_count = data.get('stealer_logs', {}).get('count', 0)
        
        # Build HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ReconPulse Report - {email}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
            color: #e0e0e0;
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }}
        .header h1 {{
            color: white;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .header .email {{
            font-size: 1.3em;
            color: #ffd700;
            font-weight: bold;
        }}
        .header .timestamp {{
            color: #ccc;
            margin-top: 10px;
            font-size: 0.9em;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .card {{
            background: #1a1f3a;
            padding: 25px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #2a3f5f;
            transition: transform 0.3s ease;
        }}
        .card:hover {{
            transform: translateY(-5px);
            border-color: #667eea;
        }}
        .card .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #ffd700;
            margin-bottom: 10px;
        }}
        .card .stat-label {{
            color: #999;
            font-size: 1.1em;
        }}
        .section {{
            margin-top: 40px;
        }}
        .section h2 {{
            border-bottom: 2px solid #667eea;
            padding-bottom: 15px;
            margin-bottom: 20px;
            color: #ffd700;
        }}
        .breach {{
            background: #2a0000;
            border-left: 4px solid #ff4444;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
        }}
        .breach strong {{
            color: #ff6666;
        }}
        .breach-item {{
            margin: 5px 0;
        }}
        footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #333;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 ReconPulse Intelligence Report</h1>
            <div class="email">{email}</div>
            <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        
        <div class="grid">
            <div class="card">
                <div class="stat-value">{risk}/100</div>
                <div class="stat-label">Risk Score</div>
            </div>
            <div class="card">
                <div class="stat-value">{breach_count}</div>
                <div class="stat-label">Data Breaches</div>
            </div>
            <div class="card">
                <div class="stat-value">{account_count}</div>
                <div class="stat-label">Discovered Accounts</div>
            </div>
            <div class="card">
                <div class="stat-value">{stealer_count}</div>
                <div class="stat-label">Stealer Logs</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📋 Breach Details</h2>
"""
        
        # Add breach data
        breaches = data.get('data_breaches', {}).get('results', [])
        if breaches:
            for breach in breaches[:50]:
                source = breach.get('source', {})
                pwd = breach.get('password', '')
                src_name = source.get('name', 'Unknown')
                src_date = source.get('date', 'N/A')
                
                html_content += f'<div class="breach">'
                html_content += f'<strong>Source:</strong> {src_name}<br>'
                if src_date:
                    html_content += f'<strong>Date:</strong> {src_date}<br>'
                if pwd:
                    masked_pwd = f"{pwd[:2]}{'*' * (len(pwd)-2)}"
                    html_content += f'<strong>Password:</strong> {masked_pwd}<br>'
                if breach.get('username'):
                    html_content += f'<strong>Username:</strong> {breach["username"]}<br>'
                html_content += '</div>'
        else:
            html_content += '<p style="color: #666;">No breaches found.</p>'
        
        html_content += """
        </div>
        
        <footer>
            <p>Report generated by ReconPulse v2.0.0 | Powered by IntelBase API</p>
        </footer>
    </div>
</body>
</html>
"""
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return str(filename)
        except Exception as e:
            raise Exception(f"Failed to write HTML: {e}")
