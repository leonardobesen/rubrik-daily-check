"""Utility module for data type conversions."""

import logging
from datetime import datetime, timedelta
from typing import Union, Optional

import pytz

from configuration.configuration import get_timezone_info
from exceptions import ConversionError

logger = logging.getLogger(__name__)

DateInput = Union[str, datetime]

def iso_to_date(date_input: DateInput, should_fix_timezone: bool = True) -> datetime:
    """
    Convert an ISO format string or datetime to a datetime object.
    
    Args:
        date_input: ISO format string or datetime object
        should_fix_timezone: Whether to convert to configured timezone
        
    Returns:
        datetime: The parsed datetime object
        
    Raises:
        ConversionError: If the conversion fails
    """
    if isinstance(date_input, datetime):
        return date_input

    if not date_input:
        raise ConversionError("Empty date input provided")

    try:
        date_obj = datetime.fromisoformat(str(date_input).replace('Z', '+00:00'))
        if should_fix_timezone:
            timezone = get_timezone_info()
            date_obj = date_obj.astimezone(pytz.timezone(timezone))
        return date_obj.replace(tzinfo=None)
    except ValueError as e:
        error_msg = f"Invalid ISO8601 format: {date_input}"
        logger.error(error_msg)
        raise ConversionError(error_msg) from e

def bytes_to_tb(bytes_size: Union[int, float]) -> float:
    """
    Convert bytes to terabytes.
    
    Args:
        bytes_size: Size in bytes
        
    Returns:
        float: Size in terabytes, rounded to 2 decimal places
        
    Raises:
        ConversionError: If the conversion fails
    """
    try:
        return round(float(bytes_size) / (1000**4), 2)
    except (TypeError, ValueError) as e:
        error_msg = f"Invalid byte size value: {bytes_size}"
        logger.error(error_msg)
        raise ConversionError(error_msg) from e

def miliseconds_to_duration(ms_value: int) -> timedelta:
    """
    Convert milliseconds to timedelta.
    
    Args:
        ms_value: Duration in milliseconds
        
    Returns:
        timedelta: Duration as timedelta object
        
    Raises:
        ConversionError: If the conversion fails
    """
    try:
        total_seconds = int(ms_value) // 1000
        return timedelta(seconds=total_seconds)
    except (TypeError, ValueError) as e:
        error_msg = f"Invalid milliseconds value: {ms_value}"
        logger.error(error_msg)
        raise ConversionError(error_msg) from e
