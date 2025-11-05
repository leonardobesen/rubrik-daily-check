"""Data operations for Rubrik Security objects."""

import logging
from typing import Optional, Dict

from model.security import ServicesAccount, SSOCertificate
from exceptions import DataProcessingError

logger = logging.getLogger(__name__)

def create_certificate_from_data(data: Dict) -> Optional[SSOCertificate]:
    """
    Create an SSOCertificate object from raw data.
    
    Args:
        data: Dictionary containing SSO certificate data
        
    Returns:
        Optional[SSOCertificate]: SSOCertificate object if successful, None if error
        
    Raises:
        DataProcessingError: If there is an error processing the data
    """
    try:
        cert_data = {
            "name": data["name"],
            "expiration_date": data["expirationDate"]
        }
        
        certificate = SSOCertificate(**cert_data)
        logger.debug(f"Successfully created SSO Certificate for {certificate.name}")
        return certificate
        
    except KeyError as e:
        error_msg = f"Missing required SSO Certificate field: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise DataProcessingError(error_msg) from e
    
    except Exception as e:
        error_msg = f"Error creating SSO Certificate: {str(e)}"
        logger.exception(error_msg)
        raise DataProcessingError(error_msg) from e

def create_service_account_from_data(data: Dict) -> Optional[ServicesAccount]:
    """
    Create a ServicesAccount object from raw data.
    
    Args:
        data: Dictionary containing service account data
        
    Returns:
        Optional[ServicesAccount]: ServicesAccount object if successful, None if error
        
    Raises:
        DataProcessingError: If there is an error processing the data
    """
    try:
        account_data = {
            "name": data["name"],
            "description": data["description"],
            "last_login": data["lastLogin"]
        }
        
        account = ServicesAccount(**account_data)
        logger.debug(f"Successfully created Service Account for {account.name}")
        return account
        
    except KeyError as e:
        error_msg = f"Missing required Service Account field: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise DataProcessingError(error_msg) from e
    
    except Exception as e:
        error_msg = f"Error creating Service Account: {str(e)}"
        logger.exception(error_msg)
        raise DataProcessingError(error_msg) from e
