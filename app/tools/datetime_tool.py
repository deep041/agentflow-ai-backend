
from datetime import datetime, timezone

def get_current_datetime() -> dict:
    return {
        "datetime": datetime.now(
            timezone.utc
        ).isoformat(),
        "timezone": "UTC",
    }
