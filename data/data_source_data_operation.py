import logging
from model.data_source import VCenter, Host

logger = logging.getLogger(__name__)


def create_vcenter_from_data(data: dict) -> VCenter | None:
    """Create a VCenter object from a dictionary of data."""
    try:
        return VCenter(
            name=data["name"],
            status=data.get("connectionStatus", {}).get("status"),
            status_message=data.get("connectionStatus", {}).get("message"),
            last_refresh_time=data.get("lastRefreshTime"),
            cluster_name=data.get("cluster", {}).get("name"),
        )
    except KeyError as e:
        logger.error(
            f"Missing expected vCenter data field: {e}", exc_info=True)
    except Exception as e:
        logger.exception(
            "Unexpected error while creating VCenter object", exc_info=True)
    return None


def create_host_from_data(data: dict) -> Host | None:
    """Create a Host object from a dictionary of data."""
    try:
        return Host(
            id=data["id"],
            name=data["name"],
            connection_status=data.get(
                "connectionStatus", {}).get("connectivity"),
            os=data.get("osType"),
            cluster_name=data.get("cluster", {}).get("name"),
        )
    except KeyError as e:
        logger.error(f"Missing expected host data field: {e}", exc_info=True)
    except Exception as e:
        logger.exception(
            "Unexpected error while creating Host object", exc_info=True)
    return None
