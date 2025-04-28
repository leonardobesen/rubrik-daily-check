import logging
from connection.wrapper import request
from model.cluster import Cluster
import graphql.cluster
from data import cluster_data_operation as data_operation

logger = logging.getLogger(__name__)


def get_all_cluster_info(access_token: str) -> list[Cluster]:
    """Fetch all clusters and enrich them with compliance information."""
    clusters = []

    try:
        query, variables = graphql.cluster.all_cluster_info_query()
        response = request(access_token, query, variables)
        nodes = response.get("data", {}).get(
            "allClusterConnection", {}).get("nodes", [])
    except Exception as e:
        logger.exception("Failed to fetch cluster data")
        raise LookupError("Unable to collect clusters data!") from e

    if not nodes:
        return []

    for item in nodes:
        cluster = data_operation.create_cluster_from_data(item)
        if cluster:
            clusters.append(cluster)

    for cluster in clusters:
        _populate_cluster_compliance(access_token, cluster)

    return clusters


def _populate_cluster_compliance(access_token: str, cluster: Cluster) -> None:
    """Fetch and set compliance information for a given cluster."""
    try:
        query, variables = graphql.cluster.cluster_compliance(cluster.id)
        response = request(access_token, query, variables)
        nodes = response.get("data", {}).get(
            "snappableGroupByConnection", {}).get("nodes", [])

        if not nodes:
            return

        in_compliance, out_of_compliance = data_operation.process_compliance_information(
            response, cluster)
        cluster_name = cluster.name.lower()

        if cluster_name in in_compliance:
            cluster.set_in_compliance_count(in_compliance[cluster_name])

        if cluster_name in out_of_compliance:
            cluster.set_out_of_compliance_count(
                out_of_compliance[cluster_name])

        data_operation.pull_compliance_time(access_token, cluster)

    except Exception as e:
        logger.warning(
            f"Failed to update compliance info for cluster {cluster.name}: {e}", exc_info=True)
