"""Controller module for handling security-related operations."""

import logging
from typing import List, Dict, Any

from connection.wrapper import request
from model.security import ServicesAccount, SSOCertificate
import graphql.security
from data import security_data_operation as data_operation
from exceptions import RubrikAPIError

logger = logging.getLogger(__name__)

def get_all_certificate_info(access_token: str) -> List[SSOCertificate]:
    """
    Retrieve all SSO certificate information from the Rubrik cluster.

    Args:
        access_token (str): Authentication token for the Rubrik API.

    Returns:
        List[SSOCertificate]: List of SSO certificate objects.

    Raises:
        RubrikAPIError: If there's an error collecting certificate data.
    """
    certificate_information: List[SSOCertificate] = []
    query = graphql.security.sso_certificate_info_query()

    try:
        response = request(access_token, query)
        if not isinstance(response, Dict) or "data" not in response:
            logger.error("Invalid response format from Rubrik API")
            return []

        providers = response["data"].get("allCurrentOrgIdentityProviders", [])
        for item in providers:
            certificate = data_operation.create_certificate_from_data(item)
            if certificate:
                certificate_information.append(certificate)
                logger.debug(f"Processed certificate for provider: {certificate.name}")

    except Exception as e:
        error_msg = "Unable to collect certificate data"
        logger.exception(error_msg)
        raise RubrikAPIError(error_msg) from e

    return certificate_information

def get_all_service_account_info(access_token: str) -> List[ServicesAccount]:
    """
    Retrieve all service account information from the Rubrik cluster.

    Args:
        access_token (str): Authentication token for the Rubrik API.

    Returns:
        List[ServicesAccount]: List of service account objects.

    Raises:
        RubrikAPIError: If there's an error collecting service account data.
    """
    accounts_information: List[ServicesAccount] = []
    query = graphql.security.service_accounts_info_query()

    try:
        response = request(access_token, query)
        if not isinstance(response, Dict) or "data" not in response:
            logger.error("Invalid response format from Rubrik API")
            return []

        nodes = response["data"].get("serviceAccounts", {}).get("nodes", [])
        for item in nodes:
            account = data_operation.create_service_account_from_data(item)
            if account:
                accounts_information.append(account)
                logger.debug(f"Processed service account: {account.username}")

    except Exception as e:
        error_msg = "Unable to collect Service Accounts data"
        logger.exception(error_msg)
        raise RubrikAPIError(error_msg) from e

    return accounts_information
