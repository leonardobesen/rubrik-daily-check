from connection.wrapper import request
from model.live_mount import LiveMount
import graphql.live_mount
from enum import Enum


class LiveMountType(Enum):
    ORACLE = "Oracle"
    MSSQL = "MSSQL"
    MANAGED_VOLUME = "Managed Volume"
    VM = "Virtual Machine"


def create_oracle_live_mount_from_data(data):
    try:
        return LiveMount(
            id=data["id"],
            name=data["sourceDatabase"]["name"],
            type=LiveMountType.ORACLE.value,
            date=data["creationDate"],
            cluster_name=data["cluster"]["name"]
        )
    except Exception as e:
        print("Error processing Oracle Live Mount item: ", e)
        return None


def create_mssql_live_mount_from_data(data):
    try:
        return LiveMount(
            id=data["fid"],
            name=data["sourceDatabase"]["name"],
            type=LiveMountType.VM.value,
            date=data["creationDate"],
            cluster_name=data["cluster"]["name"]
        )
    except Exception as e:
        print("Error processing MSSQL Live Mount item: ", e)
        return None


def create_vm_live_mount_from_data(data):
    try:
        return LiveMount(
            id=data["id"],
            name=data["sourceVm"]["name"],
            type=LiveMountType.VM.value,
            date=data["mountTimestamp"],
            cluster_name=data["cluster"]["name"]
        )
    except Exception as e:
        print("Error processing VM Live Mount item: ", e)
        return None


def create_managed_volume_mount_from_data(data):
    try:
        return LiveMount(
            id=data["id"],
            name=data["name"],
            type=LiveMountType.VM.value,
            date=data["channels"]["exportDate"],
            cluster_name=data["cluster"]["name"]
        )
    except Exception as e:
        print("Error processing MV Live Mount item: ", e)
        return None
