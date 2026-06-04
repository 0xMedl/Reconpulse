"""
Main ReconPulse Engine
"""
from .api_client import IntelBaseClient
from ..utils.constants import API_KEY, API_URL, RISK_THRESHOLDS

class ReconEngine:
    """Main investigation engine"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or API_KEY
        self.client = IntelBaseClient(self.api_key, API_URL.replace('/lookup/email', ''))
        self.current_data = None
        self.current_email = None
    
    def investigate(self, email):
        """Complete investigation"""
        result = self.client.lookup_email(email)
        
        if result["success"]:
            self.current_data = result["data"]
            self.current_email = email
            return result["data"]
        else:
            raise Exception(result.get("error", "Unknown error"))
    
    def calculate_risk(self, data=None):
        """Calculate risk score"""
        if data is None:
            data = self.current_data
        
        if not data:
            return 0
        
        score = 0
        breaches = data.get('data_breaches', {})
        score += min(breaches.get('amount', 0) * 2, 40)
        
        logs = data.get('stealer_logs', {})
        score += min(logs.get('count', 0) * 5, 30)
        
        accounts = data.get('identifier', {}).get('accounts', [])
        score += min(len(accounts), 20)
        
        timeline = data.get('meta', {}).get('timeline', [])
        score += min(len(timeline), 10)
        
        return min(score, 100)
    
    def get_risk_level(self, score):
        """Get risk level from score"""
        for level, info in RISK_THRESHOLDS.items():
            if score >= info['min']:
                return level, info['color'], info['icon']
        return "LOW", "green", "🟢"
