"""
Monitoring and Logging Utilities for AI Platform
Tracks API usage, performance metrics, and errors
"""
import logging
import time
import json
from datetime import datetime
from typing import Dict, Optional, Any
from functools import wraps
from collections import defaultdict

logger = logging.getLogger(__name__)


class APIUsageTracker:
    """Track API usage and costs"""
    
    def __init__(self):
        self.usage_stats = defaultdict(lambda: {
            'calls': 0,
            'total_input_tokens': 0,
            'total_output_tokens': 0,
            'errors': 0,
            'total_time': 0
        })
        self.start_time = datetime.now()
    
    def record_call(
        self,
        service: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        duration: float = 0,
        error: bool = False
    ):
        """Record an API call"""
        stats = self.usage_stats[service]
        stats['calls'] += 1
        stats['total_input_tokens'] += input_tokens
        stats['total_output_tokens'] += output_tokens
        stats['total_time'] += duration
        if error:
            stats['errors'] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        total_calls = sum(s['calls'] for s in self.usage_stats.values())
        total_errors = sum(s['errors'] for s in self.usage_stats.values())
        total_time = sum(s['total_time'] for s in self.usage_stats.values())
        
        # Estimate costs (Gemini pricing)
        input_cost = sum(s['total_input_tokens'] for s in self.usage_stats.values()) * 0.000075 / 1000
        output_cost = sum(s['total_output_tokens'] for s in self.usage_stats.values()) * 0.0003 / 1000
        total_cost = input_cost + output_cost
        
        return {
            'total_calls': total_calls,
            'total_errors': total_errors,
            'error_rate': (total_errors / total_calls * 100) if total_calls > 0 else 0,
            'total_time': round(total_time, 2),
            'uptime': datetime.now().isoformat(),
            'startup_time': self.start_time.isoformat(),
            'estimated_cost': round(total_cost, 6),
            'by_service': dict(self.usage_stats)
        }
    
    def reset(self):
        """Reset statistics"""
        self.usage_stats.clear()
        self.start_time = datetime.now()


class PerformanceMonitor:
    """Monitor performance metrics"""
    
    def __init__(self):
        self.metrics = {
            'image_generation': [],
            'resume_optimization': [],
            'ats_analysis': [],
            'cover_letter_generation': []
        }
    
    def record_metric(self, service: str, duration: float, success: bool = True):
        """Record a performance metric"""
        if service in self.metrics:
            self.metrics[service].append({
                'duration': duration,
                'success': success,
                'timestamp': datetime.now().isoformat()
            })
    
    def get_average_time(self, service: str) -> float:
        """Get average execution time for a service"""
        if not self.metrics[service]:
            return 0
        total = sum(m['duration'] for m in self.metrics[service])
        return round(total / len(self.metrics[service]), 3)
    
    def get_success_rate(self, service: str) -> float:
        """Get success rate for a service"""
        if not self.metrics[service]:
            return 0
        successful = sum(1 for m in self.metrics[service] if m['success'])
        return round(successful / len(self.metrics[service]) * 100, 2)
    
    def get_report(self) -> Dict[str, Any]:
        """Get performance report"""
        return {
            'by_service': {
                service: {
                    'average_time': self.get_average_time(service),
                    'success_rate': self.get_success_rate(service),
                    'total_calls': len(self.metrics[service])
                }
                for service in self.metrics.keys()
            }
        }


def track_performance(service_name: str):
    """Decorator to track performance metrics"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(f"✅ {service_name} completed in {duration:.2f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"❌ {service_name} failed after {duration:.2f}s: {str(e)}")
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(f"✅ {service_name} completed in {duration:.2f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"❌ {service_name} failed after {duration:.2f}s: {str(e)}")
                raise
        
        # Return async or sync wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


# Global instances
usage_tracker = APIUsageTracker()
performance_monitor = PerformanceMonitor()


def get_system_health() -> Dict[str, Any]:
    """Get overall system health status"""
    import psutil
    
    return {
        'status': 'healthy',
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
        'api_usage': usage_tracker.get_stats(),
        'performance': performance_monitor.get_report(),
        'timestamp': datetime.now().isoformat()
    }


import asyncio
