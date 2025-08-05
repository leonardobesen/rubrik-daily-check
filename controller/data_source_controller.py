import logging
from connection.wrapper import request
from model.data_source import VCenter, Host
import graphql.data_sources
from data import data_source_data_operation as data_operation

logger = logging.getLogger(__name__)


def get_all_vcenter_info(access_token: str) -> list[VCenter]:
    """Fetch all vCenter information."""
    try:
        query = graphql.data_sources.all_vcenters_query()
        response = request(access_token, query)

        nodes = response.get("data", {}).get(
            "vSphereVCenterConnection", {}).get("nodes", [])
    except Exception as e:
        logger.exception("Failed to fetch vCenter data")
        raise LookupError("Unable to collect vCenter data!") from e

    vcenters = []
    for item in nodes:
        vcenter = data_operation.create_vcenter_from_data(item)
        if vcenter:
            vcenters.append(vcenter)

    return vcenters


def _get_host_info_by_os(access_token: str, os_type: str) -> list[Host]:
    """Fetch disconnected hosts filtered by OS type."""
    hosts = []
    has_hosts = True
    cursor = ""

    while has_hosts:
        query, variables = graphql.data_sources.all_disconnected_hosts_query(
            os_type=os_type,
            after_value=cursor)

        try:
            response = request(access_token, query, variables)

            page_info = response.get("data", {}).get(
                "physicalHosts", {}).get("pageInfo", [])
            nodes = response.get("data", {}).get(
                "physicalHosts", {}).get("nodes", [])
        except Exception as e:
            response["data"] = None
            logger.exception(
                f"Failed to fetch all host data for OS type {os_type}")

        if not response["data"]:
            has_hosts = False
            continue

        for item in nodes:
            host = data_operation.create_host_from_data(item)
            if not host:
                continue

            hosts.append(host)

        if not page_info:
            has_hosts = False

        if page_info.get("hasNextPage", False):
            cursor = page_info.get("endCursor", "")

        if not cursor:
            has_hosts = False

    return hosts


def get_all_host_info(access_token: str) -> list[Host]:
    """Fetch all disconnected hosts across supported OS types."""
    hosts = []
    for os_type in ["NAS", "LINUX", "WINDOWS"]:
        hosts.extend(_get_host_info_by_os(access_token, os_type))
    return hosts
