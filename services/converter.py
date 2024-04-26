from datetime import datetime, timedelta
from typing import Optional


def iso_to_date(iso_str: str, correct_timezone=True) -> Optional[datetime]:
    try:
        date_obj = datetime.fromisoformat(iso_str).replace(tzinfo=None)
        if correct_timezone:
            date_obj = date_obj - timedelta(hours=3)
        return date_obj
    except ValueError:
        print(f"Invalid ISO8601 format provided")
        return None


def bytes_to_tb(bytes_size: int) -> float:
    return round(bytes_size/(1000**4), 2)


def miliseconds_to_duration(long_value: int) -> timedelta:
    total_seconds = long_value // 1000
    time_delta = timedelta(seconds=total_seconds)

    return time_delta
