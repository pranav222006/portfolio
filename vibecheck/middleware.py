import os
import time
import logging
from datetime import datetime
from collections import deque
from pathlib import Path
from django.conf import settings

# In-memory metrics ring buffer for telemetry/health dashboard
RECENT_REQUEST_LOGS = deque(maxlen=30)
REQUEST_METRICS = {
    'total_requests': 0,
    'total_errors': 0,
    'start_time': datetime.utcnow()
}

logger = logging.getLogger('vibecheck.requests')

class RequestLoggingMiddleware:
    """
    Custom Middleware for logging HTTP requests and responses.
    Fulfills assessment requirement: 'Request logging and a health check page'.
    Logs execution time, status code, IP address, and request path to file & telemetry buffer.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = getattr(settings, 'LOGS_DIR', Path('logs')) / 'requests.log'
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def __call__(self, request):
        start_time = time.time()
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '127.0.0.1')

        # Process request
        response = self.get_response(request)
        
        duration_ms = round((time.time() - start_time) * 1000, 2)
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        method = request.method
        path = request.path
        status = response.status_code

        # Update telemetry metrics
        REQUEST_METRICS['total_requests'] += 1
        if status >= 400:
            REQUEST_METRICS['total_errors'] += 1

        log_entry = {
            'timestamp': timestamp,
            'ip': ip,
            'method': method,
            'path': path,
            'status': status,
            'duration_ms': duration_ms
        }
        RECENT_REQUEST_LOGS.appendleft(log_entry)

        # Write to log file
        log_line = f"[{timestamp}] {ip} - \"{method} {path}\" {status} - {duration_ms}ms\n"
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_line)
        except Exception as e:
            logger.warning(f"Failed to write to requests log file: {e}")

        return response
