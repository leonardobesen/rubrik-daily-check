import rubrik_cdm
import datetime

def get_cluster_compliance(rubrik: rubrik_cdm.Connect, cluster_info: dict) -> list[dict]:
    # Getting compliance data from Rubrik API
    cluster_compliance = dict()
    compliance = rubrik.get('v1', '/report/compliance_summary', timeout=300)

    # Check if return wasn't empty
    if not compliance:
        return [{'clusterDatacenter': f'Unable to collect object and compliance data for {cluster_info["cluster_dc"]}'}]

    # Set cluster info name
    cluster_compliance["clusterDatacenter"] = cluster_info['cluster_dc']
    cluster_compliance["clusterName"] = cluster_info['cluster_name']
    cluster_compliance["totalObjects"] = compliance['totalProtected']
    cluster_compliance["numberOfInComplianceSnapshots"] = compliance['numberOfInComplianceSnapshots']
    cluster_compliance["numberOfOutOfComplianceSnapshots"] = compliance['numberOfOutOfComplianceSnapshots']
    cluster_compliance["percentOfInComplianceSnapshots"] = compliance['percentOfInComplianceSnapshots']
    cluster_compliance["percentOfOutOfComplianceSnapshots"] = compliance['percentOfOutOfComplianceSnapshots']
    cluster_compliance["updatedTime"] = compliance['updatedTime']

    return [cluster_compliance]

def cluster_long_running_jobs(rubrik: rubrik_cdm.Connect, cluster_info: dict) -> list[dict]:
    #Setting get params
    params = {
        "job_event_status": "Active",
        "sort_by": "StartTime",
        "sort_order": "desc"
    }

    # Get active jobs from Rubrik API order by oldest
    active_jobs = rubrik.get('v1','/job_monitoring', params=params, timeout=300)

    if not active_jobs:
        return [{'clusterDatacenter': f'No active jobs found {cluster_info["cluster_dc"]}'}]

    # Checking if jobMonitoring list exists and if it is not empty, sometimes this key cannot be there
    try:
        if not active_jobs['jobMonitoringInfoList']:
            return [{'clusterDatacenter': f'No active jobs found {cluster_info["cluster_dc"]}'}]
    except KeyError:
        return [{'clusterDatacenter': f'No active jobs found {cluster_info["cluster_dc"]}'}]

    # Looping through jobs to get which one is long running
    cluster_long_running_jobs = list()
    for job in active_jobs['jobMonitoringInfoList']:
        # Setting threshold on hours based on job type
        if job['jobType'] == 'Archival' or job['jobType'] == 'Replication':
            threshold = datetime.timedelta(hours=48)
        else:
            threshold = datetime.timedelta(hours=24)
        
        job_duration = datetime.timedelta(microseconds=job['duration'])

        if job_duration > threshold:
            # Adding Rubrik Cluster info to job
            cluster_data = {
                "clusterDatacenter": cluster_info['cluster_dc'],
                "clusterName": cluster_info['cluster_name']
            }
            # Appending cluster data to beginning of dict
            job = {**cluster_data, **job}
            cluster_long_running_jobs.append(job)
    
    if not cluster_long_running_jobs:
        cluster_long_running_jobs = [{'clusterDatacenter': f'No long running jobs found {cluster_info["cluster_dc"]}'}]

    return cluster_long_running_jobs
