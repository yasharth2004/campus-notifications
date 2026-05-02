"""
Priority Notification System for Campus Notifications Microservice
Fetches notifications from API and maintains a sorted priority inbox
"""

import heapq
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
from logging_middleware import LoggingMiddleware


class Notification:
    """Represents a single notification with priority scoring"""
    
    # Weight mapping for notification types
    TYPE_WEIGHTS = {
        "Placement": 3,
        "Result": 2,
        "Event": 1
    }
    
    def __init__(self, notification_data: Dict[str, Any]):
        self.id = notification_data.get("ID")
        self.type = notification_data.get("Type")
        self.message = notification_data.get("Message")
        self.timestamp_str = notification_data.get("Timestamp")
        
        # Parse timestamp
        self.timestamp = datetime.strptime(
            self.timestamp_str,
            "%Y-%m-%d %H:%M:%S"
        )
        
        # Calculate priority score
        self.priority_score = self._calculate_priority()
    
    def _calculate_priority(self) -> float:
        """
        Calculate priority score based on:
        1. Type weight (Placement > Result > Event)
        2. Recency (more recent = higher score)
        """
        type_weight = self.TYPE_WEIGHTS.get(self.type, 0)
        
        # Convert timestamp to numeric value for recency comparison
        # Using timestamp as secondary sort key (newer = higher)
        timestamp_numeric = self.timestamp.timestamp()
        
        # Combined priority: (type_weight * 1000000) + timestamp_numeric
        # This ensures type weight is primary, timestamp is secondary
        priority = (type_weight * 1000000) + timestamp_numeric
        
        return priority
    
    def __lt__(self, other: 'Notification') -> bool:
        """Less than comparison for heap ordering (min-heap)"""
        return self.priority_score < other.priority_score
    
    def __repr__(self) -> str:
        return (f"Notification(ID={self.id}, Type={self.type}, "
                f"Priority={self.priority_score:.0f})")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert notification to dictionary for display"""
        return {
            "ID": self.id,
            "Type": self.type,
            "Message": self.message,
            "Timestamp": self.timestamp_str,
            "PriorityScore": self.priority_score
        }


class PriorityInboxManager:
    """
    Manages the priority inbox using a min-heap for efficient
    top-n notification maintenance
    """
    
    def __init__(self, top_n: int = 10):
        self.top_n = top_n
        self.heap: List[Notification] = []
        self.logger = LoggingMiddleware("PriorityInbox")
        self.logger.log_info(f"Initialized PriorityInboxManager with top_n={top_n}")
    
    def add_notification(self, notification: Notification):
        """
        Add notification to priority inbox, maintaining only top-n.
        Uses min-heap for O(log n) insertion.
        """
        self.logger.log_debug(
            f"Adding notification: {notification.id}",
            context={
                "type": notification.type,
                "priority": notification.priority_score,
                "heap_size": len(self.heap)
            }
        )
        
        if len(self.heap) < self.top_n:
            # Heap not full yet, just add
            heapq.heappush(self.heap, notification)
            self.logger.log_debug(
                "Notification added to heap",
                context={"new_heap_size": len(self.heap)}
            )
        elif notification.priority_score > self.heap[0].priority_score:
            # New notification has higher priority than min element
            # Replace the minimum element
            removed = heapq.heapreplace(self.heap, notification)
            self.logger.log_debug(
                f"Notification replaced minimum element",
                context={
                    "removed_id": removed.id,
                    "new_notification_id": notification.id
                }
            )
        else:
            # Notification priority is lower than all in heap, skip it
            self.logger.log_debug(
                f"Notification skipped (lower priority than min in heap)",
                context={"notification_id": notification.id}
            )
    
    def get_top_notifications(self) -> List[Notification]:
        """
        Return top-n notifications sorted by priority (highest first)
        """
        self.logger.log_info(
            f"Retrieving top {len(self.heap)} notifications",
            context={"total_in_heap": len(self.heap)}
        )
        
        # Sort heap in descending order (highest priority first)
        sorted_notifications = sorted(self.heap, key=lambda x: x.priority_score, reverse=True)
        
        self.logger.log_info(
            "Top notifications retrieved and sorted",
            context={
                "count": len(sorted_notifications),
                "top_priority": sorted_notifications[0].priority_score if sorted_notifications else 0
            }
        )
        
        return sorted_notifications
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about current inbox state"""
        type_counts = {}
        for notification in self.heap:
            type_counts[notification.type] = type_counts.get(notification.type, 0) + 1
        
        return {
            "total_notifications": len(self.heap),
            "by_type": type_counts,
            "heap_capacity": self.top_n
        }


class NotificationAPI:
    """Handles communication with the Notification API"""
    
    def __init__(self, api_url: str, api_key: Optional[str] = None):
        self.api_url = api_url
        self.api_key = api_key
        self.logger = LoggingMiddleware("NotificationAPI")
        self.logger.log_info(
            "Initialized NotificationAPI",
            context={"url": api_url}
        )
    
    def fetch_notifications(self) -> List[Dict[str, Any]]:
        """
        Fetch notifications from the API
        """
        self.logger.log_info("Fetching notifications from API", context={"url": self.api_url})
        
        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.get(self.api_url, headers=headers, timeout=10)
            
            self.logger.log_debug(
                "API response received",
                context={
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds()
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                notifications = data.get("notifications", [])
                self.logger.log_info(
                    f"Successfully fetched {len(notifications)} notifications",
                    context={"count": len(notifications)}
                )
                return notifications
            else:
                self.logger.log_error(
                    f"API returned status code {response.status_code}",
                    context={
                        "status_code": response.status_code,
                        "response": response.text[:200]
                    }
                )
                return []
        
        except requests.exceptions.RequestException as e:
            self.logger.log_error(
                f"Failed to fetch notifications from API: {str(e)}",
                context={"error": str(e), "url": self.api_url}
            )
            return []


def process_notifications(
    api_url: str,
    top_n: int = 10,
    api_key: Optional[str] = None,
    use_mock: bool = False
) -> Dict[str, Any]:
    """
    Main function to fetch and prioritize notifications
    """
    logger = LoggingMiddleware("NotificationProcessor")
    logger.log_info("Starting notification processing", context={"top_n": top_n, "use_mock": use_mock})
    
    # Fetch notifications
    notifications_data = None
    
    if use_mock:
        logger.log_info("Using mock data for testing")
        from mock_data import MOCK_NOTIFICATIONS
        notifications_data = MOCK_NOTIFICATIONS.get("notifications", [])
    else:
        api = NotificationAPI(api_url, api_key)
        notifications_data = api.fetch_notifications()
    
    if not notifications_data:
        logger.log_error("No notifications fetched from API or mock data")
        return {
            "success": False,
            "message": "Failed to fetch notifications",
            "top_notifications": [],
            "statistics": {}
        }
    
    # Process notifications through priority inbox
    manager = PriorityInboxManager(top_n=top_n)
    
    logger.log_info(
        f"Processing {len(notifications_data)} notifications through priority inbox"
    )
    
    processed_count = 0
    for notification_data in notifications_data:
        try:
            notification = Notification(notification_data)
            manager.add_notification(notification)
            processed_count += 1
            logger.log_debug(f"Processed notification {notification.id}")
        except Exception as e:
            logger.log_error(
                f"Error processing notification: {str(e)}",
                context={"error": str(e), "data": str(notification_data)[:100]}
            )
    
    logger.log_info(
        f"Completed processing: {processed_count} notifications processed",
        context={"processed": processed_count, "total": len(notifications_data)}
    )
    
    # Get results
    top_notifications = manager.get_top_notifications()
    statistics = manager.get_statistics()
    
    logger.log_info("Notification processing completed successfully")
    
    return {
        "success": True,
        "message": f"Successfully prioritized {len(top_notifications)} notifications",
        "top_notifications": [n.to_dict() for n in top_notifications],
        "statistics": statistics
    }
