"""
Enhanced Error Handling and Validation Utilities
"""
import logging
from typing import Optional, Dict, Any
from functools import wraps
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class AIError(Exception):
    """Base exception for AI service errors"""
    pass


class APIKeyError(AIError):
    """Raised when API key is missing or invalid"""
    pass


class RateLimitError(AIError):
    """Raised when rate limit is exceeded"""
    pass


class APIError(AIError):
    """Raised when API call fails"""
    pass


def handle_gemini_errors(func):
    """Decorator to handle Gemini API errors gracefully"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except APIKeyError as e:
            logger.error(f"API Key Error: {str(e)}")
            raise HTTPException(
                status_code=401,
                detail="Invalid or missing Gemini API key. Please check your configuration."
            )
        except RateLimitError as e:
            logger.error(f"Rate Limit Error: {str(e)}")
            raise HTTPException(
                status_code=429,
                detail="API rate limit exceeded. Please try again later."
            )
        except APIError as e:
            logger.error(f"API Error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"AI Service Error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected Error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred. Please try again."
            )
    return wrapper


def validate_api_key(api_key: str) -> bool:
    """Validate Gemini API key format"""
    if not api_key or len(api_key) < 20:
        return False
    return True


def validate_resume_input(resume_dict: Dict[str, Any]) -> bool:
    """Validate resume input data"""
    required_fields = ['name', 'email', 'phone', 'target_role', 'skills']
    for field in required_fields:
        if field not in resume_dict or not resume_dict[field]:
            return False
    return True


def validate_job_description(job_desc: str) -> bool:
    """Validate job description"""
    return len(job_desc) > 50 and len(job_desc) < 50000


class RateLimiter:
    """Simple rate limiter for API calls"""
    def __init__(self, max_calls: int = 60, time_window: int = 60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    def is_allowed(self) -> bool:
        """Check if request is allowed"""
        import time
        now = time.time()
        # Remove old calls outside the time window
        self.calls = [call_time for call_time in self.calls 
                     if now - call_time < self.time_window]
        
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False


# Global rate limiter instance
_rate_limiter = RateLimiter()


def check_rate_limit() -> bool:
    """Check if current request is within rate limit"""
    return _rate_limiter.is_allowed()
