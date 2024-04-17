from connection.wrapper import request
from model.cluster import Cluster
import graphql.cluster

def create_cluster_from_data(data):
    try:
        return Cluster(
            id=data["id"],
            name=data["name"],
            system_status=data["systemStatus"],
            pause_status=data["pauseStatus"],
            status=data["status"],
            connected_state=data["state"]["connectedState"],
            is_connection_checked=data["passesConnectivityCheck"],
            last_connection_time=data["lastConnectionTime"],
            total_capacity=data["metric"]["totalCapacity"],
            used_capacity=data["metric"]["usedCapacity"],
            snapshot_capacity=data["metric"]["snapshotCapacity"],
            system_capacity=data["metric"]["systemCapacity"],
            available_capacity=data["metric"]["availableCapacity"],
            last_updated_time=data["metric"]["lastUpdateTime"],
            estimated_runaway=data["estimatedRunway"]
        )
    except Exception as e:
        print("Error processing cluster item: ", e)
        return None


def process_compliance_information(response):
    in_compliance = {}
    out_of_compliance = {}

    for node in response["data"]["snappableGroupByConnection"]["nodes"]:
        status = node["groupByInfo"]["ComplianceStatus"]
        cluster_group_by = node["clusterGroup"]

        for cluster in cluster_group_by:
            cluster_name = cluster["clusterInfo"]["clusterName"].lower()
            count = cluster["complianceCount"]["count"]

            if status == "IN_COMPLIANCE":
                in_compliance[cluster_name] = count
            elif status == "OUT_OF_COMPLIANCE":
                out_of_compliance[cluster_name] = count

    return in_compliance, out_of_compliance


def pull_compliance_time(access_token, cluster: Cluster):
    query, variables = graphql.cluster.cluster_compliance_pull_time_query(cluster.id)

    try:
        response = request(access_token, query, variables)
        cluster.set_compliance_pull_time(response["data"]["snappableConnection"]["edges"][0]["node"]["pullTime"])
    except:
        pass


