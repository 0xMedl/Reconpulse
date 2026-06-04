"""
Helper functions
"""
import json
import csv
from pathlib import Path
from datetime import datetime

def count_data_points(data):
    """Count all data points recursively"""
    count = 0
    def recursive_count(obj):
        nonlocal count
        if isinstance(obj, dict):
            for v in obj.values():
                if v is not None and v != "" and v != []:
                    count += 1
                recursive_count(v)
        elif isinstance(obj, list):
            for item in obj:
                recursive_count(item)
    recursive_count(data)
    return count

def sanitize_filename(email):
    """Make email safe for filenames"""
    return email.replace('@', '_').replace('.', '_')

def get_timestamp():
    """Get formatted timestamp"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")
