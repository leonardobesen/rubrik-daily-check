from datetime import datetime, timedelta
from typing import Optional
from configuration.configuration import get_timezone_info
import pytz


def iso_to_date(iso_str: str, should_fix_timezone=True) -> Optional[datetime]:
    timezone = get_timezone_info()

    try:
        date_obj = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        if should_fix_timezone:
            date_obj = date_obj.astimezone(pytz.timezone(timezone))
        return date_obj.replace(tzinfo=None)
    except ValueError:
        print(f"Invalid ISO8601 format provided")
        return None


def bytes_to_tb(bytes_size: int) -> float:
    return round(bytes_size/(1000**4), 2)


def miliseconds_to_duration(long_value: int) -> timedelta:
    total_seconds = long_value // 1000
    time_delta = timedelta(seconds=total_seconds)

    return time_delta
