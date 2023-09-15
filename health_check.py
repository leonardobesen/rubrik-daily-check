import rubrik_cdm


def cluster_health_check(rubrik: rubrik_cdm.Connect, cluster_info: dict) -> list[dict]:
    cluster_health_check = dict()

    # Getting cluster status from Rubrik API
    cluster_health_check = rubrik.get(
        'internal', '/cluster/me/system_status', timeout=300)

    # Checking with return wasn't empty
    if not cluster_health_check:
        return [{'clusterDatacenter': f'Unable to collect health check data for {cluster_info["cluster_dc"]}'}]

    # Appending cluster data to beginning of dict
    cluster_info_dict = {
        "clusterDatacenter": cluster_info['cluster_dc'],
        "clusterName": cluster_info['cluster_name']
    }
    cluster_health_check = {**cluster_info_dict, **cluster_health_check}

    return [cluster_health_check]
