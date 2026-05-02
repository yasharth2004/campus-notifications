import json
import sys
from typing import Optional
from notification_priority_system import process_notifications
from logging_middleware import LoggingMiddleware


def display_results(result: dict):
    """Display results in a formatted manner"""
    logger = LoggingMiddleware("DisplayResults")
    
    logger.log_info("=" * 80)
    logger.log_info("CAMPUS NOTIFICATIONS - PRIORITY INBOX")
    logger.log_info("=" * 80)
    
    if not result["success"]:
        logger.log_error(f"Failed to process notifications: {result['message']}")
        return
    stats = result["statistics"]
    logger.log_info(f"Statistics - Total in Inbox: {stats['total_notifications']}/{stats['heap_capacity']}")
    
    type_breakdown = stats.get("by_type", {})
    for notif_type, count in sorted(type_breakdown.items()):
        logger.log_info(f"  - {notif_type}: {count}")
    
    logger.log_info("-" * 80)
    logger.log_info(f"TOP {stats['total_notifications']} PRIORITIZED NOTIFICATIONS:")
    logger.log_info("-" * 80)
    notifications = result["top_notifications"]
    for rank, notif in enumerate(notifications, 1):
        logger.log_info(f"\n[RANK #{rank}]")
        logger.log_info(f"  ID: {notif['ID']}")
        logger.log_info(f"  Type: {notif['Type']}")
        logger.log_info(f"  Message: {notif['Message']}")
        logger.log_info(f"  Timestamp: {notif['Timestamp']}")
        logger.log_info(f"  Priority Score: {notif['PriorityScore']:.0f}")
    
    logger.log_info("\n" + "=" * 80)
    logger.log_info("END OF PRIORITY INBOX")
    logger.log_info("=" * 80)
    
    # Also save JSON output for documentation
    with open("priority_inbox_output.json", "w") as f:
        json.dump(result, indent=2, fp=f)
    logger.log_info("Output saved to priority_inbox_output.json")


def main(api_key: Optional[str] = None, use_mock: bool = False):
    """
    Main function to run the priority inbox system
    """
    logger = LoggingMiddleware("Main")
    logger.log_info("Starting Campus Notifications Priority Inbox System")
    
    # API Configuration
    API_URL = "http://20.207.122.201/evaluation-service/notifications"
    TOP_N = 10
    
    logger.log_info(
        "Configuration loaded",
        context={
            "api_url": API_URL,
            "top_n": TOP_N,
            "has_api_key": api_key is not None,
            "use_mock": use_mock
        }
    )
    
    # Process notifications
    result = process_notifications(
        api_url=API_URL,
        top_n=TOP_N,
        api_key=api_key,
        use_mock=use_mock
    )
    
    # Display results
    display_results(result)
    
    logger.log_info("Priority Inbox System execution completed")
    
    return result


if __name__ == "__main__":
    # Parse command line arguments
    api_key = None
    use_mock = False
    
    for arg in sys.argv[1:]:
        if arg == "--mock":
            use_mock = True
        elif arg.startswith("--key="):
            api_key = arg.split("=", 1)[1]
        elif arg != "--mock":
            api_key = arg
    
    if use_mock:
        print("Using mock data for testing (no API call)")
    elif api_key:
        print("Using provided API key")
    else:
        print("No API key provided. Attempting to fetch without authentication...")
        print("Tip: Use --mock flag to test with sample data")
    
    result = main(api_key=api_key, use_mock=use_mock)
    
    # Exit with appropriate code
    sys.exit(0 if result["success"] else 1)
