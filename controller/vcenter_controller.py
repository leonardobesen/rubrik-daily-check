from connection.wrapper import request
from model.vcenter import VCenter
import graphql.data_sources
from data import vcenter_data_operation as data_operation



def get_all_vcenter_info(access_token: str) -> list[VCenter]:
    vcenter_information = []

    # Gather clusters information
    query = graphql.data_sources.all_vcenters_query()

    try:
        response = request(access_token, query)
    except Exception:
        raise LookupError("Unable to collect vcenter data!")

    if not response["data"]["vSphereVCenterConnection"]["nodes"]:
        return []

    # Process cluster information
    for item in response["data"]["vSphereVCenterConnection"]["nodes"]:
        vcenter = data_operation.create_vcenter_from_data(item)
        if vcenter:
            vcenter_information.append(vcenter)

    return vcenter_information