"""Controller module for managing data source operations with Rubrik."""

import logging
from typing import List, Dict, Any, Optional
from enum import Enum, auto

from connection.wrapper import request
from model.data_source import VCenter, Host
import graphql.data_sources
from data import data_source_data_operation as data_operation
from exceptions import RubrikAPIError

logger = logging.getLogger(__name__)


class OSType(Enum):
    """Supported operating system types for hosts."""
    NAS = auto()
    LINUX = auto()
    WINDOWS = auto()


def get_all_vcenter_info(access_token: str) -> List[VCenter]:
    """
    Fetch all vCenter information from the Rubrik cluster.

    Args:
        access_token: Authentication token for the Rubrik API

    Returns:
        List of VCenter objects containing vCenter information

    Raises:
        RubrikAPIError: If there's an error collecting vCenter data
    """
    query = graphql.data_sources.all_vcenters_query()
    response = request(access_token, query)

    if not isinstance(response, Dict) or "data" not in response:
        logger.error("Invalid response format from Rubrik API")
        return []

    nodes = response.get("data", {}).get(
        "vSphereVCenterConnection", {}).get("nodes", [])

    vcenters = []
    for item in nodes:
        try:
            vcenter = data_operation.create_vcenter_from_data(item)
            if vcenter:
                vcenters.append(vcenter)
                logger.debug(f"Processed vCenter: {vcenter.name}")
        except Exception:
            error_msg = "Failed to fetch vCenter data"
            logger.exception(error_msg)
            continue

    return vcenters


def _get_host_info_by_os(access_token: str, os_type: str) -> List[Host]:
    """
    Fetch disconnected hosts filtered by OS type.

    Args:
        access_token: Authentication token for the Rubrik API
        os_type: Type of operating system to filter hosts by

    Returns:
        List of Host objects for the specified OS type

    Raises:
        RubrikAPIError: If there's an error collecting host data
    """
    hosts: List[Host] = []
    has_hosts = True
    cursor: Optional[str] = ""

    while has_hosts:
        try:
            query, variables = graphql.data_sources.all_disconnected_hosts_query(
                os_type=os_type,
                after_value=cursor
            )
            response = request(access_token, query, variables)

            if not isinstance(response, Dict) or "data" not in response:
                logger.error(f"Invalid response format for {os_type} hosts")
                break

            data = response["data"].get("physicalHosts", {})
            page_info = data.get("pageInfo", {})
            nodes = data.get("nodes", [])

            for item in nodes:
                host = data_operation.create_host_from_data(item)
                if host:
                    hosts.append(host)
                    logger.debug(f"Processed {os_type} host: {host.name}")

            # Check if there are more pages
            if not page_info or not page_info.get("hasNextPage", False):
                break

            cursor = page_info.get("endCursor")
            if not cursor:
                break

        except Exception as e:
            logger.error(f"Failed to fetch {os_type} host data: {str(e)}")
            break

    return hosts


def get_all_host_info(access_token: str) -> List[Host]:
    """
    Fetch all disconnected hosts across supported OS types.

    Args:
        access_token: Authentication token for the Rubrik API

    Returns:
        List of all Host objects across different OS types

    Note:
        Continues processing even if one OS type fails
    """
    hosts: List[Host] = []

    for os_type in OSType:
        try:
            os_hosts = _get_host_info_by_os(access_token, os_type.name)
            hosts.extend(os_hosts)
            logger.info(f"Successfully collected {len(os_hosts)} {os_type.name} hosts")
        except Exception as e:
            logger.error(f"Failed to collect {os_type.name} hosts: {str(e)}")
            continue

    return hosts
