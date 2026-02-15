"""
Utility Helper Functions
Common utilities used across the application
"""
from datetime import datetime, timedelta
import json


def format_date(date_string, format_str='%Y-%m-%d'):
    """
    Format ISO date string to readable format
    
    Args:
        date_string (str): ISO format date string
        format_str (str): Desired output format
        
    Returns:
        str: Formatted date string
    """
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        return date_obj.strftime(format_str)
    except (ValueError, TypeError):
        return date_string


def calculate_date_range(days_back=90):
    """
    Calculate date range for analysis
    
    Args:
        days_back (int): Number of days to look back
        
    Returns:
        tuple: (start_date, end_date) as datetime objects
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    return start_date, end_date


def safe_divide(numerator, denominator, default=0):
    """
    Safely divide two numbers, returning default if denominator is 0
    
    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Default value if division by zero
        
    Returns:
        float: Result of division or default
    """
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default


def truncate_text(text, max_length=100, suffix='...'):
    """
    Truncate text to maximum length
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        suffix (str): Suffix to add if truncated
        
    Returns:
        str: Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def save_json(data, filename):
    """
    Save data to JSON file
    
    Args:
        data: Data to save
        filename (str): Output filename
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(filename):
    """
    Load data from JSON file
    
    Args:
        filename (str): Input filename
        
    Returns:
        dict: Loaded data
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def validate_github_username(username):
    """
    Validate GitHub username format
    
    Args:
        username (str): Username to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not username:
        return False
    
    # GitHub username rules:
    # - May only contain alphanumeric characters or hyphens
    # - Cannot have multiple consecutive hyphens
    # - Cannot begin or end with a hyphen
    # - Maximum 39 characters
    
    if len(username) > 39:
        return False
    
    if username.startswith('-') or username.endswith('-'):
        return False
    
    if '--' in username:
        return False
    
    return all(c.isalnum() or c == '-' for c in username)


def percentage(part, whole, decimal_places=2):
    """
    Calculate percentage
    
    Args:
        part: Part value
        whole: Whole value
        decimal_places (int): Number of decimal places
        
    Returns:
        float: Percentage value
    """
    if whole == 0:
        return 0.0
    return round((part / whole) * 100, decimal_places)
