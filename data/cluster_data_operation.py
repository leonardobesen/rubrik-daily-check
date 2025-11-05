"""Data operations for Rubrik clusters."""

import logging
from typing import Optional, Tuple, Dict
from dataclasses import asdict

from connection.wrapper import request
from model.cluster import Cluster
import graphql.cluster
from exceptions import DataProcessingError

logger = logging.getLogger(__name__)

def create_cluster_from_data(data: Dict) -> Optional[Cluster]:
    """
    Create a Cluster object from API response data.
    
    Args:
        data: Dictionary containing cluster data from API
        
    Returns:
        Optional[Cluster]: Cluster object if successful, None if error
        
    Raises:
        DataProcessingError: If required data is missing or invalid
    """
    try:
        # Extract metrics data for better readability
        metrics = data.get("metric", {})
        state = data.get("state", {})
        
        cluster_data = {
            "id": data["id"],
            "name": data["name"],
            "system_status": data["systemStatus"],
            "pause_status": data["pauseStatus"],
            "status": data["status"],
            "connected_state": state.get("connectedState"),
            "passed_connection_test": data.get("passesConnectivityCheck", False),
            "last_connection_time": data.get("lastConnectionTime"),
            "total_capacity": metrics.get("totalCapacity", 0),
            "used_capacity": metrics.get("usedCapacity", 0),
            "snapshot_capacity": metrics.get("snapshotCapacity", 0),
            "system_capacity": metrics.get("systemCapacity", 0),
            "available_capacity": metrics.get("availableCapacity", 0),
            "last_updated_time": metrics.get("lastUpdateTime"),
            "estimated_runaway": data.get("estimatedRunway", 0)
        }
        
        # Create cluster instance using our dataclass
        cluster = Cluster(**cluster_data)
        logger.debug(f"Successfully created Cluster object for {cluster.name}")
        return cluster
        
    except KeyError as e:
        error_msg = f"Missing required cluster data field: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise DataProcessingError(error_msg) from e
        
    except Exception as e:
        error_msg = f"Error creating Cluster object: {str(e)}"
        logger.exception(error_msg)
        raise DataProcessingError(error_msg) from e


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
