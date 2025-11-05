"""Data operations for Rubrik Live Mount objects."""

import logging
from typing import Optional, Dict

from model.live_mount import LiveMount, MountType
from exceptions import DataProcessingError

logger = logging.getLogger(__name__)

def create_oracle_live_mount_from_data(data: Dict) -> Optional[LiveMount]:
    """
    Create a LiveMount object from Oracle data.
    
    Args:
        data: Dictionary containing Oracle Live Mount data
        
    Returns:
        Optional[LiveMount]: LiveMount object if successful, None if error
    """
    try:
        mount_data = {
            "id": data["id"],
            "name": data["sourceDatabase"]["name"],
            "type": MountType.ORACLE,
            "date": data["creationDate"],
            "cluster_name": data["cluster"]["name"]
        }
        
        mount = LiveMount(**mount_data)
        logger.debug(f"Successfully created Oracle Live Mount for {mount.name}")
        return mount
        
    except KeyError as e:
        error_msg = f"Missing required Oracle Live Mount field: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise DataProcessingError(error_msg) from e
    
    except Exception as e:
        error_msg = f"Error creating Oracle Live Mount: {str(e)}"
        logger.exception(error_msg)
        raise DataProcessingError(error_msg) from e

def create_mssql_live_mount_from_data(data: Dict) -> Optional[LiveMount]:
    """Create a LiveMount object from MSSQL data."""
    try:
        mount_data = {
            "id": data["fid"],
            "name": data["sourceDatabase"]["name"],
            "type": MountType.MSSQL,
            "date": data["creationDate"],
            "cluster_name": data["cluster"]["name"]
        }
        
        mount = LiveMount(**mount_data)
        logger.debug(f"Successfully created MSSQL Live Mount for {mount.name}")
        return mount
        
    except KeyError as e:
        error_msg = f"Missing required MSSQL Live Mount field: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise DataProcessingError(error_msg) from e
    
    except Exception as e:
        error_msg = f"Error creating MSSQL Live Mount: {str(e)}"
        logger.exception(error_msg)
        raise DataProcessingError(error_msg) from e

def create_vm_live_mount_from_data(data: Dict) -> Optional[LiveMount]:
    """Create a LiveMount object from VM data."""
    try:
        mount_data = {
            "id": data["id"],
            "name": data["sourceVm"]["name"],
            "type": MountType.VM,
            "date": data["mountTimestamp"],
            "cluster_name": data["cluster"]["name"]
        }
        
        mount = LiveMount(**mount_data)
        logger.debug(f"Successfully created VM Live Mount for {mount.name}")
        return mount
        
    except KeyError as e:
        error_msg = f"Missing required VM Live Mount field: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise DataProcessingError(error_msg) from e
    
    except Exception as e:
        error_msg = f"Error creating VM Live Mount: {str(e)}"
        logger.exception(error_msg)
        raise DataProcessingError(error_msg) from e

def create_managed_volume_mount_from_data(data: Dict) -> Optional[LiveMount]:
    """Create a LiveMount object from Managed Volume data."""
    try:
        mount_data = {
            "id": data["id"],
            "name": data["name"],
            "type": MountType.MANAGED_VOLUME,
            "date": data["channels"][0]["exportDate"],
            "cluster_name": data["cluster"]["name"]
        }
        
        mount = LiveMount(**mount_data)
        logger.debug(f"Successfully created Managed Volume Mount for {mount.name}")
        return mount
        
    except KeyError as e:
        error_msg = f"Missing required Managed Volume Mount field: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise DataProcessingError(error_msg) from e
    
    except Exception as e:
        error_msg = f"Error creating Managed Volume Mount: {str(e)}"
        logger.exception(error_msg)
        raise DataProcessingError(error_msg) from e
