"""
Helper utility functions
"""
import uuid
import hashlib
from datetime import datetime
from typing import Optional

def generate_unique_id() -> str:
    """Generate a unique identifier"""
    return str(uuid.uuid4())

def generate_short_id() -> str:
    """Generate a short unique identifier (8 characters)"""
    return str(uuid.uuid4())[:8]

def get_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.now().isoformat()

def get_file_extension(filename: str) -> str:
    """Extract file extension from filename"""
    return filename.split('.')[-1].lower() if '.' in filename else ''

def sanitize_path(path: str) -> str:
    """Sanitize file path to prevent directory traversal"""
    return path.replace('..', '').replace('/', '').replace('\\', '')

def calculate_file_hash(content: bytes) -> str:
    """Calculate SHA-256 hash of file content"""
    return hashlib.sha256(content).hexdigest()