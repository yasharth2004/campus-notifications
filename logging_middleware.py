
import logging
import json
from datetime import datetime
from typing import Any, Dict


class LoggingMiddleware:
    def __init__(self, name: str = "CampusNotifications"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_info(self, message: str, context: Dict[str, Any] = None):
        if context:
            message = f"{message} | Context: {json.dumps(context)}"
        self.logger.info(message)
    
    def log_debug(self, message: str, context: Dict[str, Any] = None):
        
        if context:
            message = f"{message} | Context: {json.dumps(context)}"
        self.logger.debug(message)
    
    def log_error(self, message: str, context: Dict[str, Any] = None):
        if context:
            message = f"{message} | Context: {json.dumps(context)}"
        self.logger.error(message)
    
    def log_warning(self, message: str, context: Dict[str, Any] = None):
        if context:
            message = f"{message} | Context: {json.dumps(context)}"
        self.logger.warning(message)
    
    def log_event(self, event_type: str, details: Dict[str, Any]):
        event_log = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details
        }
        self.logger.info(f"EVENT: {json.dumps(event_log)}")
