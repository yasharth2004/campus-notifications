"""
Custom Logging Middleware for Campus Notifications System
Provides structured logging with severity levels and timestamps
"""

import logging
import json
from datetime import datetime
from typing import Any, Dict


class LoggingMiddleware:
    """
    Centralized logging middleware for the Campus Notifications Microservice.
    Ensures all operations are logged with structured format.
    """
    
    def __init__(self, name: str = "CampusNotifications"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler with formatting
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        
        # Custom formatter for structured logs
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_info(self, message: str, context: Dict[str, Any] = None):
        """Log info level message with optional context"""
        if context:
            message = f"{message} | Context: {json.dumps(context)}"
        self.logger.info(message)
    
    def log_debug(self, message: str, context: Dict[str, Any] = None):
        """Log debug level message with optional context"""
        if context:
            message = f"{message} | Context: {json.dumps(context)}"
        self.logger.debug(message)
    
    def log_error(self, message: str, context: Dict[str, Any] = None):
        """Log error level message with optional context"""
        if context:
            message = f"{message} | Context: {json.dumps(context)}"
        self.logger.error(message)
    
    def log_warning(self, message: str, context: Dict[str, Any] = None):
        """Log warning level message with optional context"""
        if context:
            message = f"{message} | Context: {json.dumps(context)}"
        self.logger.warning(message)
    
    def log_event(self, event_type: str, details: Dict[str, Any]):
        """Log a specific event with type and details"""
        event_log = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details
        }
        self.logger.info(f"EVENT: {json.dumps(event_log)}")
