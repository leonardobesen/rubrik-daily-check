import rubrik_cdm


def cluster_vcenter_status(rubrik: rubrik_cdm.Connect, cluster_info: dict) -> list[dict]:
    # Get storage info
    vcenters = rubrik.get(
        'v1', '/vmware/vcenter?primary_cluster_id=local', timeout=300)

    # Checking with return wasn't empty
    if not vcenters:
        return [{'clusterName': f'Unable to collect health check data for {cluster_info["cluster_dc"]}'}]

    vcenters_status = []
    for vcenter in vcenters['data']:
        vcenter_placeholder = {}
        vcenter_placeholder["clusterDatacenter"] = cluster_info['cluster_dc']
        vcenter_placeholder["clusterName"] = cluster_info['cluster_name']
        vcenter_placeholder["vcenterName"] = vcenter["name"]
        vcenter_placeholder["hostname"] = vcenter["hostname"]
        vcenter_placeholder["status"] = vcenter["connectionStatus"]["status"]
        vcenter_placeholder["lastRefresh"] = vcenter["lastRefreshTime"]
        vcenters_status.append(vcenter_placeholder)

    return vcenters_status


def cluster_nas_disconnected(rubrik: rubrik_cdm.Connect, cluster_info: dict) -> list[dict]:
    # Query NAS share info
    nas_info = rubrik.get('internal', '/host/share', timeout=300)

    if not nas_info:
        return [{'clusterDatacenter': f'Unable to collect Nas Share data for {cluster_info["cluster_dc"]}'}]

    if not nas_info["data"]:
        return [{'clusterDatacenter': f'No NAS Shares found on {cluster_info["cluster_dc"]}'}]

    nas_disconnected = []
    for nas in nas_info["data"]:
        if nas["status"] == "Connected":
            continue

        nas_data = {}
        nas_data["clusterDatacenter"] = cluster_info["cluster_dc"]
        nas_data["clusterName"] = cluster_info['cluster_name']
        nas_data["shareType"] = nas["shareType"]
        nas_data["hostname"] = nas["hostname"]
        nas_data["exportPoint"] = nas["exportPoint"]
        nas_data["status"] = nas["status"]
        nas_disconnected.append(nas_data)

    return nas_disconnected


def cluster_api_status(rubrik: rubrik_cdm.Connect, cluster_info: dict) -> list[dict]:
    # Get user id
    user_info = rubrik.get('internal', '/user/me', timeout=300)
    if not user_info:
        return [{'clusterDatacenter': f'Unable to collect API data for {cluster_info["cluster_dc"]}'}]

    user_id = user_info["id"].removeprefix("User:::")

    # Query APIs for that user
    param = {
        "user_id": user_id,
    }
    api_tokens = rubrik.get('internal', '/session', params=param, timeout=300)

    if not api_tokens:
        return [{'clusterDatacenter': f'Unable to collect API data for {cluster_info["cluster_dc"]}'}]

    if not api_tokens["data"]:
        return [{'clusterDatacenter': f'No API Tokens found on {cluster_info["cluster_dc"]}!!!'}]

    tokens = []
    for api_token in api_tokens["data"]:
        token = {}
        token["clusterDatacenter"] = cluster_info["cluster_dc"]
        token["clusterName"] = cluster_info['cluster_name']
        token["name"] = api_token["tag"]
        token["creationTime"] = api_token["creationTime"]
        token["lastUsageTime"] = api_token["lastUsageTime"]
        token["expirationTime"] = api_token["expirationTime"]
        tokens.append(token)

    return tokens


def cluster_certificate_status(rubrik: rubrik_cdm.Connect, cluster_info: dict) -> list[dict]:
    # Get storage info
    certificates = rubrik.get('v1', '/idp_auth_domain', timeout=300)

    # Checking with return wasn't empty
    if not certificates:
        return [{'clusterDatacenter': f'Unable to collect Certificate data for {cluster_info["cluster_dc"]}'}]

    ad_status = {}
    for cert in certificates['data']:
        if cert['name'] == "azure_ad" or cert['name'] == "azure-ad":
            ad_status["clusterDatacenter"] = cluster_info['cluster_dc']
            ad_status["clusterName"] = cluster_info['cluster_name']
            ad_status["name"] = cert["name"]
            ad_status["expireDate"] = cert["signCertExpiryDate"]

    # If no azure_ad mostly likely means it was removed
    if not ad_status:
        return [{'clusterDatacenter': f'No Azure AD Certificate found for {cluster_info["cluster_dc"]}!!!'}]

    return [ad_status]
