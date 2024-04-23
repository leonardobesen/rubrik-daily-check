from connection.wrapper import request
from model.cluster import Cluster
import graphql.cluster
from data import cluster_data_operation as data_operation


def get_all_cluster_info(access_token: str) -> list[Cluster]:
    clusters_information = []

    # Gather clusters information
    query, variables = graphql.cluster.all_cluster_info_query()

    try:
        response = request(access_token, query, variables)
    except Exception:
        raise LookupError("Unable to collect clusters data!")

    if not response["data"]:
        return []

    # Process cluster information
    for item in response["data"]["allClusterConnection"]["nodes"]:
        cluster = data_operation.create_cluster_from_data(item)
        if cluster:
            clusters_information.append(cluster)

    # Gather clusters compliance information
    query, variables = graphql.cluster.all_clusters_compliance()

    try:
        response = request(access_token, query, variables)
    except Exception:
        pass

    if response["data"]["snappableGroupByConnection"]["nodes"]:
        in_compliance, out_of_compliance = data_operation.process_compliance_information(
            response)
        for cluster in clusters_information:
            cluster_name_lower = cluster.name.lower()

            if cluster_name_lower in in_compliance:
                cluster.set_in_compliance_count(
                    in_compliance[cluster_name_lower])

            if cluster_name_lower in out_of_compliance:
                cluster.set_out_of_compliance_count(
                    out_of_compliance[cluster_name_lower])

            data_operation.pull_compliance_time(access_token, cluster)

    return clusters_information
