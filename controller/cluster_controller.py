"""Controller module for managing Rubrik cluster operations."""

import logging
from typing import List, Dict, Any, Tuple

from connection.wrapper import request
from model.cluster import Cluster
import graphql.cluster
from data import cluster_data_operation as data_operation
from exceptions import RubrikAPIError

logger = logging.getLogger(__name__)

def get_all_cluster_info(access_token: str) -> List[Cluster]:
    """
    Fetch all clusters and enrich them with compliance information.

    Args:
        access_token: Authentication token for the Rubrik API

    Returns:
        List of Cluster objects with enriched compliance information

    Raises:
        RubrikAPIError: If there's an error collecting cluster data
    """
    try:
        clusters = _fetch_basic_cluster_info(access_token)
        for cluster in clusters:
            try:
                _populate_cluster_compliance(access_token, cluster)
            except Exception as e:
                logger.error(
                    f"Failed to fetch compliance info for cluster {cluster.name}: {str(e)}"
                )
                # Continue processing other clusters even if one fails
        return clusters

    except Exception as e:
        error_msg = "Failed to fetch cluster data"
        logger.exception(error_msg)
        raise RubrikAPIError(error_msg) from e

def _fetch_basic_cluster_info(access_token: str) -> List[Cluster]:
    """
    Fetch basic information for all clusters.

    Args:
        access_token: Authentication token for the Rubrik API

    Returns:
        List of Cluster objects with basic information

    Raises:
        RubrikAPIError: If there's an error collecting cluster data
    """
    query, variables = graphql.cluster.all_cluster_info_query()
    response = request(access_token, query, variables)

    if not isinstance(response, Dict) or "data" not in response:
        logger.error("Invalid response format from Rubrik API")
        return []

    nodes = response.get("data", {}).get(
        "allClusterConnection", {}).get("nodes", [])

    if not nodes:
        logger.info("No clusters found in the response")
        return []

    clusters = []
    for item in nodes:
        cluster = data_operation.create_cluster_from_data(item)
        if cluster:
            clusters.append(cluster)
            logger.debug(f"Processed cluster: {cluster.name}")

    return clusters

def _populate_cluster_compliance(access_token: str, cluster: Cluster) -> None:
    """
    Fetch and set compliance information for a given cluster.

    Args:
        access_token: Authentication token for the Rubrik API
        cluster: Cluster object to update with compliance information

    Raises:
        ValueError: If the cluster data is invalid
        RubrikAPIError: If there's an error collecting compliance data
    """
    if not cluster.id or not cluster.name:
        raise ValueError("Invalid cluster data: missing id or name")

    try:
        # Fetch compliance data
        query, variables = graphql.cluster.cluster_compliance(cluster.id)
        response = request(access_token, query, variables)

        if not isinstance(response, Dict) or "data" not in response:
            logger.error(f"Invalid compliance response for cluster {cluster.name}")
            return

        nodes = response.get("data", {}).get(
            "snappableGroupByConnection", {}).get("nodes", [])

        if not nodes:
            logger.info(f"No compliance data found for cluster {cluster.name}")
            return

        # Process compliance information
        in_compliance, out_of_compliance = data_operation.process_compliance_information(
            response, cluster
        )
        cluster_name = cluster.name.lower()

        # Update cluster compliance counts
        if cluster_name in in_compliance:
            cluster.set_in_compliance_count(in_compliance[cluster_name])
            logger.debug(f"Updated in-compliance count for {cluster.name}")

        if cluster_name in out_of_compliance:
            cluster.set_out_of_compliance_count(out_of_compliance[cluster_name])
            logger.debug(f"Updated out-of-compliance count for {cluster.name}")

        # Update compliance time
        data_operation.pull_compliance_time(access_token, cluster)
        logger.debug(f"Updated compliance time for {cluster.name}")

    except Exception as e:
        error_msg = f"Failed to update compliance info for cluster {cluster.name}"
        logger.error(f"{error_msg}: {str(e)}", exc_info=True)
        raise RubrikAPIError(error_msg) from e
