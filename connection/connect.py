"""Legacy connection module for backward compatibility."""

import logging
from typing import Optional

from connection.client import RubrikClient
from exceptions import RubrikAPIError

logger = logging.getLogger(__name__)

# Global client instance for backward compatibility
_client: Optional[RubrikClient] = None

def get_client() -> RubrikClient:
    """
    Get or create the global RubrikClient instance.
    
    Returns:
        RubrikClient: The global client instance
    """
    global _client
    if not _client:
        _client = RubrikClient()
    return _client

def open_session() -> str:
    """
    Open a new session with the Rubrik API.
    
    Returns:
        str: The access token for the session
        
    Raises:
        RubrikAPIError: If authentication fails
    """
    try:
        client = get_client()
        return client.authenticate()
    except Exception as e:
        logger.exception("Failed to open session")
        raise RubrikAPIError("Failed to authenticate with Rubrik API") from e

def close_session(access_token: str) -> None:
    """
    Close an existing session with the Rubrik API.
    
    Args:
        access_token: The access token to invalidate
        
    Raises:
        RubrikAPIError: If logout fails
    """
    try:
        client = get_client()
        client._access_token = access_token  # Set token directly for backward compatibility
        client.logout()
    except Exception as e:
        logger.exception("Failed to close session")
        raise RubrikAPIError("Failed to logout from Rubrik API") from e
