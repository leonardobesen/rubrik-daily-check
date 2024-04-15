from connection.wrapper import request
from query_builder import cluster as query_builder

def get_all_cluster_info(access_token: str) -> list[dict]:
    clusters_information = []
    query, variables = query_builder.all_cluster_info_query()

    try:
        response = request(access_token, query, variables)
        for item in response["data"]["allClusterConnection"]["nodes"]:
            clusters_information.append(item)
    except:
        return []

    return clusters_information