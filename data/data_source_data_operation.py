"""Data operations for Rubrik data sources."""

import logging
from typing import Optional, Dict

from model.data_source import VCenter, Host, ConnectionStatus, OSType
from exceptions import DataProcessingError

logger = logging.getLogger(__name__)

def create_vcenter_from_data(data: Dict) -> Optional[VCenter]:
    """
    Create a VCenter object from API response data.
    
    Args:
        data: Dictionary containing vCenter data from API
        
    Returns:
        Optional[VCenter]: VCenter object if successful, None if error
        
    Raises:
        DataProcessingError: If required data is missing or invalid
    """
    try:
        conn_status = data.get("connectionStatus", {})
        vcenter_data = {
            "name": data["name"],
            "status": conn_status.get("status", "UNKNOWN"),
            "status_message": conn_status.get("message", ""),
            "last_refresh_time": data.get("lastRefreshTime"),
            "cluster_name": data.get("cluster", {}).get("name", "unknown")
        }
        
        vcenter = VCenter(**vcenter_data)
        logger.debug(f"Successfully created VCenter object for {vcenter.name}")
        return vcenter
        
    except KeyError as e:
        error_msg = f"Missing required vCenter data field: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise DataProcessingError(error_msg) from e
        
    except Exception as e:
        error_msg = f"Error creating VCenter object: {str(e)}"
        logger.exception(error_msg)
        raise DataProcessingError(error_msg) from e

def create_host_from_data(data: Dict) -> Optional[Host]:
    """
    Create a Host object from API response data.
    
    Args:
        data: Dictionary containing host data from API
        
    Returns:
        Optional[Host]: Host object if successful, None if error
        
    Raises:
        DataProcessingError: If required data is missing or invalid
    """
    try:
        host_data = {
            "id": data["id"],
            "name": data["name"],
            "connection_status": data.get("connectionStatus", {}).get("connectivity", "UNKNOWN"),
            "os": data.get("osType", "UNKNOWN"),
            "cluster_name": data.get("cluster", {}).get("name", "unknown")
        }
        
        host = Host(**host_data)
        logger.debug(f"Successfully created Host object for {host.name}")
        return host
        
    except KeyError as e:
        error_msg = f"Missing required host data field: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise DataProcessingError(error_msg) from e
        
    except Exception as e:
        error_msg = f"Error creating Host object: {str(e)}"
        logger.exception(error_msg)
        raise DataProcessingError(error_msg) from e
