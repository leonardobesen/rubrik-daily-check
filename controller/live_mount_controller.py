from connection.wrapper import request
from model.live_mount import LiveMount
import graphql.live_mount
from data import live_mount_data_operation as data_operation
from typing import Callable


def get_live_mount_info(access_token: str,
                        query_func: Callable,
                        data_key: str,
                        data_operation_func: Callable) -> list[LiveMount]:
    live_mounts_information = []

    query, variables = query_func()

    try:
        response = request(access_token, query, variables)
    except Exception:
        raise LookupError("Unable to collect live mounts data!")

    if response["data"] and data_key in response["data"]:
        for item in response["data"][data_key]["nodes"]:
            live_mount = data_operation_func(item)

            if not live_mount:
                continue

            live_mounts_information.append(live_mount)

    return live_mounts_information


def get_all_live_mounts_info(access_token: str) -> list[LiveMount]:
    live_mounts_information = []

    # Gather Oracle info
    live_mounts_information.extend(
        get_live_mount_info(
            access_token,
            graphql.live_mount.oracle_live_mount_query,
            "oracleLiveMounts",
            data_operation.create_oracle_live_mount_from_data
        )
    )

    # Gather VM info
    live_mounts_information.extend(
        get_live_mount_info(
            access_token,
            graphql.live_mount.vm_live_mount_query,
            "vSphereLiveMounts",
            data_operation.create_vm_live_mount_from_data
        )
    )

    # Gather MSSQL info
    live_mounts_information.extend(
        get_live_mount_info(
            access_token,
            graphql.live_mount.mssql_live_mount_query,
            "mssqlDatabaseLiveMounts",
            data_operation.create_mssql_live_mount_from_data
        )
    )

    # Gather Managed Volume info
    live_mounts_information.extend(
        get_live_mount_info(
            access_token,
            graphql.live_mount.managed_volume_live_mount_query,
            "managedVolumeLiveMounts",
            data_operation.create_managed_volume_mount_from_data
        )
    )

    return live_mounts_information
