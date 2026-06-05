#!/usr/bin/env python3
"""
Configuration constants and API keys
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_KEY = os.getenv("INTELBASE_API_KEY", "in_0P1izKBm3tKlXsnMmPwD")
API_URL = "https://api.intelbase.is/lookup/email"

# Risk scoring thresholds
RISK_THRESHOLDS = {
    "CRITICAL": {"min": 80, "color": "red", "icon": "🔴"},
    "HIGH": {"min": 60, "color": "yellow", "icon": "🟠"},
    "MEDIUM": {"min": 40, "color": "cyan", "icon": "🟡"},
    "LOW": {"min": 0, "color": "green", "icon": "🟢"}
}

# Important account information fields
IMPORTANT_ACCOUNT_FIELDS = [
    'username', 'user_id', 'id', 'full_name', 'display_name',
    'creation_date', 'last_login_date', 'profile_url', 'location', 'city',
    'followers', 'following', 'premium_status', 'is_verified', 'status',
    'country', 'bio', 'avatar_url', 'gender', 'birthday', 'email'
]
