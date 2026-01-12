"""
Security utilities (for future authentication/authorization)
"""
from datetime import datetime, timedelta
from typing import Optional
import hashlib

def generate_hash(content: str) -> str:
    """Generate SHA256 hash of content"""
    return hashlib.sha256(content.encode()).hexdigest()

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal attacks"""
    # Remove any path components
    filename = filename.replace("/", "").replace("\\", "")
    # Remove any null bytes
    filename = filename.replace("\0", "")
    return filename

def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """Validate file extension"""
    ext = filename.split('.')[-1].lower()
    return ext in allowed_extensions