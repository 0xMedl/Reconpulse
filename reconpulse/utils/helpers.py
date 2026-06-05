#!/usr/bin/env python3
"""
Utility helper functions
"""

import json
import csv
from pathlib import Path
from datetime import datetime


def count_data_points(data):
    """Recursively count all non-empty data points in the investigation data"""
    point_count = 0
    
    def _traverse(obj):
        nonlocal point_count
        
        if isinstance(obj, dict):
            for value in obj.values():
                # Count non-empty values
                if value is not None and value != "" and value != []:
                    point_count += 1
                # Recurse into nested structures
                _traverse(value)
        
        elif isinstance(obj, list):
            for item in obj:
                _traverse(item)
    
    _traverse(data)
    return point_count


def sanitize_filename(email):
    """Convert email to safe filename by replacing special characters"""
    # Replace @ with _ and . with _
    safe_name = email.replace('@', '_').replace('.', '_')
    return safe_name


def get_timestamp():
    """Get current timestamp in standardized format"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")
