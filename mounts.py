import rubrik_cdm

def cluster_live_mounts(rubrik: rubrik_cdm.Connect, cluster_info: dict) -> list[dict]:
    # Defining list of dicts with keys: "clusterName", "clusterDatacenter", "id", "tech", "name" and "mountTimestamp"
    mounts = []
    # Get mounts from Rubrik API and concatenate lists
    # VMs
    vm_mount_list = _get_mounted_vm(rubrik, cluster_info)
    if vm_mount_list: mounts += vm_mount_list
    # Windows Volume Groups
    vg_mount_list = _get_mounted_vg(rubrik, cluster_info)
    if vm_mount_list: mounts += vg_mount_list
    # SQL Databases
    sql_mount_list = _get_mounted_sql(rubrik, cluster_info)
    if sql_mount_list: mounts += sql_mount_list
    # Oracle Database
    oracle_mount_list = _get_mounted_oracle(rubrik, cluster_info)
    if oracle_mount_list: mounts += oracle_mount_list
    # Managed Volumes
    mv_mount_list = _get_mounted_mv(rubrik, cluster_info)
    if mv_mount_list: mounts += mv_mount_list

    # TODO: Add code to unmount mounts older than 7 days

    if not mounts:
        return [{'clusterDatacenter': f'No Live Mounts found for {cluster_info["cluster_dc"]}'}]

    return mounts

def unmount_live_mounts(rubrik: rubrik_cdm.Connect, mounts: list[dict]) -> bool:
    # To remove a Live Mount send a DELETE request to /vmware/vm/snapshot/mount/{id}
    return False

def _get_mounted_vm(rubrik: rubrik_cdm.Connect, cluster_info: dict) -> list[dict]:
    vm_list = []

    vm_mounts = rubrik.get('v1','/vmware/vm/snapshot/mount', timeout=300)

    if vm_mounts["total"] > 0:
        for vm in vm_mounts['data']:
            vm_data = {}            
            vm_data["clusterDatacenter"] = cluster_info['cluster_dc']
            vm_data["clusterName"] = cluster_info['cluster_name']
            vm_data["id"] = vm["id"]
            vm_data["tech"] = "VM"
            vm_data["name"] = vm["datastoreName"]
            vm_data["mountTimestamp"] = vm["mountTimestamp"]
            vm_list.append(vm_data)
            
    return vm_list

def _get_mounted_vg(rubrik: rubrik_cdm.Connect, cluster_info: dict) -> list[dict]:
    vg_list = []

    vg_mounts = rubrik.get('v1','/volume_group/snapshot/mount', timeout=300)

    if vg_mounts["total"] > 0:
        for vg in vg_mounts['data']:
            vg_data = {}
            vg_data["clusterDatacenter"] = cluster_info['cluster_dc']
            vg_data["clusterName"] = cluster_info['cluster_name']
            vg_data["id"] = vg["id"]
            vg_data["tech"] = "VolumeGroup"
            vg_data["name"] = vg["sourceHostName"]
            vg_data["mountTimestamp"] = vg["mountedDate"]
            vg_list.append(vg_data)

    return vg_list

def _get_mounted_sql(rubrik: rubrik_cdm.Connect, cluster_info: dict) -> list[dict]:
    sql_list = []

    sql_mounts = rubrik.get('v1','/mssql/db/mount', timeout=300)

    if sql_mounts["total"] > 0:
        for sql in sql_mounts['data']:
            sql_data = {}
            sql_data["clusterDatacenter"] = cluster_info['cluster_dc']
            sql_data["clusterName"] = cluster_info['cluster_name']
            sql_data["id"] = sql["id"]
            sql_data["tech"] = "SQL"
            sql_data["name"] = sql["sourceDatabaseId"]
            sql_data["mountTimestamp"] = sql["creationDate"]
            sql_list.append(sql_data)
    
    return sql_list

def _get_mounted_oracle(rubrik: rubrik_cdm.Connect, cluster_info: dict) -> list[dict]:
    oracle_list = []

    oracle_mounts = rubrik.get('internal','/oracle/db/mount', timeout=300)

    if oracle_mounts["total"] > 0:
        for oracle in oracle_mounts['data']:
            oracle_data = {}            
            oracle_data["clusterDatacenter"] = cluster_info['cluster_dc']
            oracle_data["clusterName"] = cluster_info['cluster_name']
            oracle_data["id"] = oracle["id"]
            oracle_data["tech"] = "Oracle"
            oracle_data["name"] = oracle["sourceDatabaseName"]
            oracle_data["mountTimestamp"] = oracle["creationDate"]
            oracle_list.append(oracle_data)
    
    return oracle_list

def _get_mounted_mv(rubrik: rubrik_cdm.Connect, cluster_info: dict) -> list[dict]:
    mv_list = []

    mv_mounts = rubrik.get('internal','/managed_volume/snapshot/export', timeout=300)

    if mv_mounts["total"] > 0:
        for mv in mv_mounts['data']:
            mv_data = {}
            mv_data["clusterDatacenter"] = cluster_info['cluster_dc']
            mv_data["clusterName"] = cluster_info['cluster_name']
            mv_data["id"] = mv["id"]
            mv_data["tech"] = "ManagedVolume"
            mv_data["name"] = mv["sourceManagedVolumeName"]
            mv_data["mountTimestamp"] = mv["exportedDate"]
            mv_list.append(mv_data)

    return mv_list
