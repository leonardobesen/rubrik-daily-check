"""Legacy wrapper module for backward compatibility."""

import logging
from typing import Dict, Any, Optional

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

def request(access_token: str, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Legacy wrapper for making GraphQL requests.
    
    Args:
        access_token: The access token for authentication
        query: The GraphQL query string
        variables: Optional variables for the GraphQL query
        
    Returns:
        The JSON response from the API
        
    Raises:
        RubrikAPIError: If the request fails
    """
    client = get_client()
    client._access_token = access_token  # Set token directly for backward compatibility
    
    try:
        return client.graphql_request(query, variables)
    except Exception as e:
        logger.exception("GraphQL request failed")
        raise RubrikAPIError(str(e)) from e
