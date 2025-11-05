"""Controller module for handling live mount operations."""

import logging
from typing import Callable, List, Dict, Any, TypeVar, Union, Tuple

from connection.wrapper import request
from model.live_mount import LiveMount
import graphql.live_mount
from data import live_mount_data_operation as data_operation
from exceptions import RubrikAPIError

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=LiveMount)
QueryFunc = Callable[[], Tuple[str, Dict[str, Any]]]
DataOperationFunc = Callable[[Dict[str, Any]], T]

def get_live_mount_info(
    access_token: str,
    query_func: QueryFunc,
    data_key: str,
    data_operation_func: DataOperationFunc
) -> List[T]:
    """
    Generic function to fetch live mount information of a specific type.

    Args:
        access_token: Authentication token for the Rubrik API
        query_func: Function that returns the GraphQL query and variables
        data_key: Key to access the relevant data in the API response
        data_operation_func: Function to process each data item into a LiveMount object

    Returns:
        List of LiveMount objects of the specified type

    Raises:
        RubrikAPIError: If there's an error collecting live mount data
    """
    live_mounts_information: List[T] = []
    mount_type = data_key.replace("LiveMounts", "").replace("Database", "")

    try:
        query, variables = query_func()
        response = request(access_token, query, variables)

        if not isinstance(response, Dict) or "data" not in response:
            logger.error(f"Invalid response format for {mount_type} live mounts")
            return []

        nodes = response["data"].get(data_key, {}).get("nodes", [])
        for item in nodes:
            live_mount = data_operation_func(item)
            if live_mount:
                live_mounts_information.append(live_mount)
                logger.debug(f"Processed {mount_type} live mount: {live_mount.id}")

    except Exception as e:
        error_msg = f"Unable to collect {mount_type} live mounts data"
        logger.exception(error_msg)
        raise RubrikAPIError(error_msg) from e

    return live_mounts_information

def get_all_live_mounts_info(access_token: str) -> List[LiveMount]:
    """
    Retrieve all live mount information from various sources.

    Args:
        access_token: Authentication token for the Rubrik API

    Returns:
        List of all LiveMount objects across different types

    Raises:
        RubrikAPIError: If there's an error collecting any live mount data
    """
    live_mounts_information: List[LiveMount] = []
    mount_types = [
        (
            graphql.live_mount.oracle_live_mount_query,
            "oracleLiveMounts",
            data_operation.create_oracle_live_mount_from_data
        ),
        (
            graphql.live_mount.vm_live_mount_query,
            "vSphereLiveMounts",
            data_operation.create_vm_live_mount_from_data
        ),
        (
            graphql.live_mount.mssql_live_mount_query,
            "mssqlDatabaseLiveMounts",
            data_operation.create_mssql_live_mount_from_data
        ),
        (
            graphql.live_mount.managed_volume_live_mount_query,
            "managedVolumeLiveMounts",
            data_operation.create_managed_volume_mount_from_data
        )
    ]

    for query_func, data_key, data_op_func in mount_types:
        try:
            mounts = get_live_mount_info(access_token, query_func, data_key, data_op_func)
            live_mounts_information.extend(mounts)
            logger.info(f"Successfully collected {len(mounts)} {data_key}")
        except RubrikAPIError as e:
            logger.error(f"Failed to collect {data_key}: {str(e)}")
            # Continue with other mount types even if one fails

    return live_mounts_information
