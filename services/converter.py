from datetime import datetime


def iso_to_date(iso_str: str):
    try:
        date_obj = datetime.fromisoformat(iso_str)
        return date_obj.replace(tzinfo=None)
    except ValueError:
        print(f"Invalid ISO8601 format provided")
        return None


def bytes_to_tb(bytes_size: int):
    return round(bytes_size/(1000**4), 2)
