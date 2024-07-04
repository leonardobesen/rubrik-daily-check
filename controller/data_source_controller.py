from connection.wrapper import request
from model.data_source import VCenter, Host
import graphql.data_sources
from data import data_source_data_operation as data_operation


def get_all_vcenter_info(access_token: str) -> list[VCenter]:
    vcenter_information = []

    # Gather clusters information
    query = graphql.data_sources.all_vcenters_query()

    try:
        response = request(access_token, query)
    except Exception:
        raise LookupError("Unable to collect vcenter data!")

    if not response["data"]:
        return []

    # Process cluster information
    for item in response["data"]["vSphereVCenterConnection"]["nodes"]:
        vcenter = data_operation.create_vcenter_from_data(item)
        if vcenter:
            vcenter_information.append(vcenter)

    return vcenter_information


def _get_host_info_by_os(access_token: str, os_type: str) -> list[Host]:
    query, variables = graphql.data_sources.all_disconnected_hosts_query(
        os_type=os_type)

    try:
        response = request(access_token, query, variables)
    except Exception:
        raise LookupError(f"Unable to collect {os_type} data!")

    if not response["data"]:
        return []

    host_information = []
    for item in response["data"]["physicalHosts"]["nodes"]:
        host = data_operation.create_host_from_data(item)
        if host:
            host_information.append(host)

    return host_information


def get_all_host_info(access_token: str) -> list[Host]:
    host_information = []

    for os_type in ["NAS", "LINUX", "WINDOWS"]:
        host_information.extend(_get_host_info_by_os(access_token, os_type))

    return host_information
