"""
API dependencies (for future use with database, auth, etc.)
"""
from typing import Generator
import logging

logger = logging.getLogger(__name__)

def get_logger() -> logging.Logger:
    """Get logger instance"""
    return logger