"""
Validation Utilities for Deep Research System

Common validation functions for lead data, URLs, and other inputs.
"""

import re
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """
    Validate if a string is a valid URL.
    
    Args:
        url: URL string to validate
    
    Returns:
        True if valid URL, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def validate_email(email: str) -> bool:
    """
    Validate if a string is a valid email address.
    
    Args:
        email: Email string to validate
    
    Returns:
        True if valid email, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """
    Validate if a string is a valid phone number.
    
    Args:
        phone: Phone string to validate
    
    Returns:
        True if valid phone, False otherwise
    """
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    # Check if it has 10-15 digits (international format)
    return 10 <= len(digits_only) <= 15

def validate_lead_data(lead_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Validate lead data and return validation errors.
    
    Args:
        lead_data: Dictionary containing lead information
    
    Returns:
        Dictionary with validation errors (empty if valid)
    """
    errors = {}
    
    # Required fields
    required_fields = ['company_name', 'person_name']
    for field in required_fields:
        if not lead_data.get(field) or not str(lead_data[field]).strip():
            errors.setdefault('required', []).append(f"{field} is required")
    
    # Optional field validation
    if lead_data.get('email') and not validate_email(lead_data['email']):
        errors.setdefault('email', []).append("Invalid email format")
    
    if lead_data.get('website') and not validate_url(lead_data['website']):
        errors.setdefault('website', []).append("Invalid website URL")
    
    if lead_data.get('linkedin') and not validate_url(lead_data['linkedin']):
        errors.setdefault('linkedin', []).append("Invalid LinkedIn URL")
    
    if lead_data.get('phone') and not validate_phone(lead_data['phone']):
        errors.setdefault('phone', []).append("Invalid phone number format")
    
    return errors

def sanitize_input(text: str) -> str:
    """
    Sanitize user input by removing potentially harmful characters.
    
    Args:
        text: Input text to sanitize
    
    Returns:
        Sanitized text
    """
    if not isinstance(text, str):
        return str(text)
    
    # Remove control characters and excessive whitespace
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    
    return sanitized

def validate_company_size(size: str) -> bool:
    """
    Validate company size classification.
    
    Args:
        size: Company size string
    
    Returns:
        True if valid size, False otherwise
    """
    valid_sizes = ['small', 'medium', 'large', 'startup', 'enterprise']
    return size.lower() in valid_sizes

def validate_industry(industry: str) -> bool:
    """
    Validate industry classification.
    
    Args:
        industry: Industry string
    
    Returns:
        True if valid industry, False otherwise
    """
    # Common industries - can be expanded
    valid_industries = [
        'technology', 'healthcare', 'finance', 'manufacturing',
        'retail', 'education', 'government', 'non-profit',
        'agriculture', 'energy', 'transportation', 'real-estate',
        'consulting', 'media', 'telecommunications'
    ]
    return industry.lower() in valid_industries