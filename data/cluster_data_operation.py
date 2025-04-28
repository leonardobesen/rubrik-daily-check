import logging
from connection.wrapper import request
from model.cluster import Cluster
import graphql.cluster

logger = logging.getLogger(__name__)


def create_cluster_from_data(data: dict) -> Cluster | None:
    """Create a Cluster object from a dictionary of data."""
    try:
        return Cluster(
            id=data["id"],
            name=data["name"],
            system_status=data["systemStatus"],
            pause_status=data["pauseStatus"],
            status=data["status"],
            connected_state=data.get("state", {}).get("connectedState"),
            passed_connection_test=data.get("passesConnectivityCheck"),
            last_connection_time=data.get("lastConnectionTime"),
            total_capacity=data.get("metric", {}).get("totalCapacity"),
            used_capacity=data.get("metric", {}).get("usedCapacity"),
            snapshot_capacity=data.get("metric", {}).get("snapshotCapacity"),
            system_capacity=data.get("metric", {}).get("systemCapacity"),
            available_capacity=data.get("metric", {}).get("availableCapacity"),
            last_updated_time=data.get("metric", {}).get("lastUpdateTime"),
            estimated_runaway=data.get("estimatedRunway")
        )
    except KeyError as e:
        logger.error(
            f"Missing expected cluster data field: {e}", exc_info=True)
    except Exception as e:
        logger.exception(
            "Unexpected error while creating Cluster object", exc_info=True)
    return None


def process_compliance_information(response: dict, cluster: Cluster) -> tuple[dict, dict]:
    """Process compliance information from a response."""
    in_compliance = {}
    out_of_compliance = {}

    nodes = response.get("data", {}).get(
        "snappableGroupByConnection", {}).get("nodes", [])
    if not nodes:
        logger.warning(f"No compliance nodes found for cluster {cluster.name}")
        return in_compliance, out_of_compliance

    cluster_name = cluster.name.lower()

    for node in nodes:
        try:
            status = node["groupByInfo"]["enumValue"]
            count = node["snappableConnection"]["count"]

            if status == "IN_COMPLIANCE":
                in_compliance[cluster_name] = count
            elif status == "OUT_OF_COMPLIANCE":
                out_of_compliance[cluster_name] = count

        except KeyError as e:
            logger.error(
                f"Missing expected field in compliance node: {e}", exc_info=True)

    return in_compliance, out_of_compliance


def pull_compliance_time(access_token: str, cluster: Cluster) -> None:
    """Fetch and set the last compliance pull time for a cluster."""
    try:
        query, variables = graphql.cluster.cluster_compliance_pull_time_query(
            cluster.id)
        response = request(access_token, query, variables)

        edges = response.get("data", {}).get(
            "snappableConnection", {}).get("edges", [])
        if edges:
            pull_time = edges[0]["node"].get("pullTime")
            if pull_time:
                cluster.set_compliance_pull_time(pull_time)
            else:
                logger.warning(f"No pullTime found for cluster {cluster.name}")
        else:
            logger.warning(
                f"No edges found when pulling compliance time for cluster {cluster.name}")

    except Exception as e:
        logger.error(
            f"Failed to pull compliance time for cluster {cluster.name}: {e}", exc_info=True)
