from connection.wrapper import request
from model.data_source import VCenter, Nas
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


def get_all_nas_info(access_token: str) -> list[Nas]:
    nas_information = []

    # Gather clusters information
    query, variables = graphql.data_sources.all_disconnected_nas_systems_query()

    try:
        response = request(access_token, query, variables)
    except Exception:
        raise LookupError("Unable to collect NAS data!")

    if not response["data"]:
        return []

    # Process cluster information
    for item in response["data"]["physicalHosts"]["nodes"]:
        nas = data_operation.create_nas_from_data(item)
        if nas:
            nas_information.append(nas)

    return nas_information
