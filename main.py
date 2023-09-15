import json
import os
import connect
import capacity
import health_check
import jobs
import mounts
import expire
import status
import write_to_csv

# Global variables
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = write_to_csv.create_file(ROOT_DIR)

# Getting list of Rubrik clusters from JSON
with open('config.json', 'r') as json_file:
    config_parse = json.load(json_file)

# List to be appended
cluster_capacity = []
cluster_health_check = []
cluster_live_mounts = []
cluster_compliance = []
cluster_vcenter_status = []
cluster_nas_disconnected = []
cluster_long_running_jobs = []
cluster_expired_sql_dbs = []
cluster_api_age = []
cluster_certificate_age = []


# Looping through clusters to perform daily check
for cluster in config_parse['clusters']:
    # Establish connection with Rubrik CDM
    rubrik_conn = connect.connect_to_cluster(
        cluster['cluster_address'], cluster['api_token'])

    # Get Rubrik CDM name
    cluster['cluster_name'] = rubrik_conn.get('internal', '/cluster/me/name')

    print(f"Fetching data from {cluster['cluster_dc']}")
    # 1. Validate capacity, health check cluster and unmount Live Mounts +7 days old
    cluster_capacity += capacity.get_cluster_capacity(rubrik_conn, cluster)
    cluster_health_check += health_check.cluster_health_check(
        rubrik_conn, cluster)
    cluster_live_mounts += mounts.cluster_live_mounts(rubrik_conn, cluster)

    # 2. Validade total number of objects, vCenter connections and NAS Share connections
    cluster_compliance += jobs.get_cluster_compliance(rubrik_conn, cluster)
    cluster_vcenter_status += status.cluster_vcenter_status(
        rubrik_conn, cluster)
    cluster_nas_disconnected += status.cluster_nas_disconnected(
        rubrik_conn, cluster)

    # 3. Validate jobs taking more than 24 hours to complete and remove SLA/expire immediately SQL databases agreed upon
    cluster_long_running_jobs += jobs.cluster_long_running_jobs(
        rubrik_conn, cluster)
    # TODO: TO BE IMPLEMENTED (Disruptive change)
    cluster_expired_sql_dbs += expire.cluster_remove_sql_dbs(
        rubrik_conn, cluster)

    # 4. Validate for aging API Tokens and AD certificates
    cluster_certificate_age += status.cluster_certificate_status(
        rubrik_conn, cluster)
    cluster_api_age += status.cluster_api_status(rubrik_conn, cluster)

# Send data somewhere
write_to_csv.update_report(
    REPORT_FILE=FILE_PATH,
    Capacity=cluster_capacity,
    Cluster_Health_Check=cluster_health_check,
    Live_Mounts=cluster_live_mounts,
    Num_Objects=cluster_compliance,
    vCenter_Status=cluster_vcenter_status,
    API_Token_Status=cluster_api_age,
    AD_Certificate_Status=cluster_certificate_age,
    NAS_Disconnected=cluster_nas_disconnected,
    Long_Running_Jobs=cluster_long_running_jobs,
    SQL_DBs_Removed_from_Backups=cluster_expired_sql_dbs
)
