import rubrik_cdm

def get_cluster_capacity(rubrik: rubrik_cdm.Connect, cluster_info: dict) -> list[dict]:
    cluster_capacity = {}

    # Get storage info
    capacity = rubrik.get('internal','/stats/system_storage', timeout=300)

    # Return nothing if API call fails
    if not capacity:
        return [{'clusterDatacenter': f'Unable to collect capacity data for {cluster_info["cluster_dc"]}'}]
    
    # Set cluster info name
    cluster_capacity["clusterDatacenter"] = cluster_info['cluster_dc']
    cluster_capacity["clusterName"] = cluster_info['cluster_name']

    # Converting values to TBs 
    cluster_capacity["total"] = round(capacity["total"] / (1000**4), 1)
    cluster_capacity["used"] = round(capacity["used"] / (1000**4), 1)
    cluster_capacity["snapshot"] = round(capacity["snapshot"] / (1000**4), 1)
    cluster_capacity["system"] = round(capacity["miscellaneous"] / (1000**4), 1)
    cluster_capacity["available"] = round(capacity["available"] / (1000**4), 1)

    # Calculating cluster % capacity and getting update date
    cluster_capacity["pct_Available"] = round((cluster_capacity["available"] / cluster_capacity["total"]) * 100)
    cluster_capacity["lastUpdateTime"] = capacity["lastUpdateTime"]

    #TODO: implement function to get archival data consumption 
    # (implement a diferrent function to get this data and send it to a different place)

    return [cluster_capacity]
