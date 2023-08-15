import rubrik_cdm

def cluster_health_check(rubrik: rubrik_cdm.Connect, cluster_info: dict) -> list[dict]:
    cluster_health_check = dict()

    # Getting cluster status from Rubrik API
    cluster_health_check = rubrik.get('internal', '/cluster/me/system_status', timeout=300)

    # Checking with return wasn't empty
    if not cluster_health_check:
        return [{'clusterDatacenter': f'Unable to collect health check data for {cluster_info["cluster_dc"]}'}]

    # Appending cluster data to beginning of dict
    cluster_info_dict = {
        "clusterDatacenter": cluster_info['cluster_dc'],
        "clusterName": cluster_info['cluster_name']
    }
    cluster_health_check = {**cluster_info_dict, **cluster_health_check}

    # Check if nodes affected Exists and which one has failed disks
    cluster_health_check["nodesWithDisksFailure"] = set()
    try: 
        if cluster_health_check['affectedNodeIds']: 
            # Check disk status for each node
            for node in cluster_health_check["affectedNodeIds"]:
                # Get and parse disk info from each node
                disks = rubrik.get('internal', '/cluster/{node}/disk'.format(node=node))
                # Check if disks are degraded or status are not OK
                for disk in disks['data']:
                    if disk['isDegraded'] or not disk['status'] == 'OK':
                        # Register nodes with disk failure
                        cluster_health_check["nodesWithDisksFailure"].add(node)
    except KeyError:
        cluster_health_check["nodesWithDisksFailure"] = "Nenhuma falha encontrada"

    # Runs the hw_health command on all nodes in the Rubrik cluster and returns its output.
    # cluster_health_check["hw_health_check"] = rubrik.get('internal', '/cluster/me/hardware_health')

    return [cluster_health_check]
