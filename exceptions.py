"""Custom exceptions for the Rubrik Daily Check application."""

class RubrikError(Exception):
    """Base exception for Rubrik-related errors."""
    pass

class RubrikAPIError(RubrikError):
    """Raised when there's an error communicating with the Rubrik API."""
    pass

class ConfigurationError(RubrikError):
    """Raised when there's an error with the configuration."""
    pass

class DataProcessingError(RubrikError):
    """Raised when there's an error processing data."""
    pass

class ConversionError(RubrikError):
    """Raised when there's an error converting data types."""
    pass