import requests
from connection.wrapper import request
from query_builder import unmanaged_objects as query_builder

def get_all_unmanaged_objects(access_token: str, cluster_id: str) -> list[dict]:
    objects_with_local_storage = []
    query, variables = query_builder.all_unmanaged_objects_by_cluster(cluster_id)

    response = request(access_token, query, variables)

    for item in response["data"]["unmanagedObjects"]["edges"]:
        if item["node"]["localStorage"] > 0 and \
            item["node"]["isRemote"] == False:
            objects_with_local_storage.append(item["node"])

    return objects_with_local_storage