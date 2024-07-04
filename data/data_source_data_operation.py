from model.data_source import VCenter, Host


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


def create_host_from_data(data):
    try:
        return Host(
            id=data["id"],
            name=data["name"],
            connection_status=data["connectionStatus"]["connectivity"],
            os=data["osType"],
            cluster_name=data["cluster"]["name"]
        )
    except Exception as e:
        print("Error processing Host item: ", e)
        return None