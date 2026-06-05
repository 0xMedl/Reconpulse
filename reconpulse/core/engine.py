#!/usr/bin/env python3

from .api_client import IntelBaseClient
from ..utils.constants import API_KEY, API_URL, RISK_THRESHOLDS


class ReconEngine:
    """Main investigation engine for OSINT analysis"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or API_KEY
        # Remove /lookup/email from base URL to get domain
        base_domain = API_URL.replace('/lookup/email', '')
        self.client = IntelBaseClient(self.api_key, base_domain)
        self.current_data = None
        self.current_email = None
    
    def investigate(self, email):
        """Run full investigation on email address"""
        result = self.client.lookup_email(email)
        
        if result["success"]:
            self.current_data = result["data"]
            self.current_email = email
            return result["data"]
        else:
            error = result.get("error", "Unknown error occurred")
            raise Exception(error)
    
    def calculate_risk(self, data=None):
        """Calculate risk score based on investigation data"""
        if data is None:
            data = self.current_data
        
        if not data:
            return 0
        
        score = 0
        
        # Factor: data breaches (max 40 pts)
        breaches = data.get('data_breaches', {})
        breach_count = breaches.get('amount', 0)
        score += min(breach_count * 2, 40)
        
        # Factor: stealer logs (max 30 pts)
        stealer = data.get('stealer_logs', {})
        log_count = stealer.get('count', 0)
        score += min(log_count * 5, 30)
        
        # Factor: account discovery (max 20 pts)
        accounts = data.get('identifier', {}).get('accounts', [])
        score += min(len(accounts), 20)
        
        # Factor: timeline events (max 10 pts)
        timeline = data.get('meta', {}).get('timeline', [])
        score += min(len(timeline), 10)
        
        # Ensure score doesn't exceed 100
        return min(score, 100)
    
    def get_risk_level(self, score):
        """Determine risk level and associated styling from score"""
        for level, info in RISK_THRESHOLDS.items():
            if score >= info['min']:
                return level, info['color'], info['icon']
        
        # Default fallback
        return "LOW", "green", "🟢"
