from model.data_source import VCenter, Nas


def create_vcenter_from_data(data):
    try:
        return VCenter(
            name=data["name"],
            status=data["connectionStatus"]["status"],
            status_message=data["connectionStatus"]["message"],
            last_refresh_time=data["lastRefreshTime"],
            cluster_name=data["cluster"]["name"]
        )
    except Exception as e:
        print("Error processing vCenter item: ", e)
        return None


def create_nas_from_data(data):
    try:
        return Nas(
            id=data["id"],
            name=data["name"],
            connection_status=data["connectionStatus"]["connectivity"],
            cluster_name=data["cluster"]["name"]
        )
    except Exception as e:
        print("Error processing NAS item: ", e)
        return None