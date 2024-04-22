from model.vcenter import VCenter


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