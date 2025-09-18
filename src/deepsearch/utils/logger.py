"""
Logging Configuration for Deep Research System

Centralized logging setup with proper formatting and levels.
"""

import logging
import sys
from typing import Optional
from .config import config

def setup_logging(
    level: Optional[str] = None,
    format_string: Optional[str] = None,
    include_timestamp: bool = True
) -> logging.Logger:
    """
    Setup logging configuration for the Deep Research System.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom format string for log messages
        include_timestamp: Whether to include timestamp in log messages
    
    Returns:
        Configured logger instance
    """
    
    # Use config level if not specified
    if level is None:
        level = config.log_level
    
    # Default format string
    if format_string is None:
        if include_timestamp:
            format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        else:
            format_string = '%(name)s - %(levelname)s - %(message)s'
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/deepsearch.log', mode='a')
        ]
    )
    
    # Create and return logger
    logger = logging.getLogger('deepsearch')
    logger.info(f"Logging initialized with level: {level}")
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Module name (usually __name__)
    
    Returns:
        Logger instance
    """
    return logging.getLogger(f'deepsearch.{name}')