from configuration.configuration import get_excluded_clusters_uuids

def all_cluster_info_query() -> tuple[str, dict]:
    variables = {
        "filter": {
            "productFilters": [
              {
                "productType": "CDM"
              }
            ],
            "excludeId": get_excluded_clusters_uuids()
        }
    }

    query = f"""query ListAllClustersInfo($filter: ClusterFilterInput,$sortBy: ClusterSortByEnum = ClusterName){{
      allClusterConnection(filter: $filter, sortBy: $sortBy){{
        nodes{{
          id
          name
          systemStatus
          pauseStatus
          status
          state{{
            connectedState
          }}
          passesConnectivityCheck
          lastConnectionTime
          metric{{
            totalCapacity
            usedCapacity
            snapshotCapacity
            systemCapacity: miscellaneousCapacity
            availableCapacity
            lastUpdateTime
          }}
          estimatedRunway
        }}
      }}
    }}"""

    return query, variables



def cluster_compliance(cluster_id: str):
    variables = {
      "id": [cluster_id],
      "slaTimeRange": "LAST_24_HOURS"
    }

    query = f"""query ClusterComplianceQuery($id: [UUID!], $slaTimeRange: SlaComplianceTimeRange) {{
      snappableGroupByConnection(
        filter: {{cluster: {{id: $id}}, slaTimeRange: $slaTimeRange}}
        groupBy: ComplianceStatus
      ) {{
        ...ComplianceChartFragment
      }}
    }}

    fragment ComplianceChartFragment on SnappableGroupByConnection {{
      nodes {{
        groupByInfo {{
          ... on ComplianceStatus {{
            enumValue
          }}
        }}
        snappableConnection {{
          count
        }}
      }}
    }}
    """

    return query, variables


def cluster_compliance_pull_time_query(cluster_id: str) -> tuple[str, dict]:
    variables = {
        "filter": {
            "cluster": {
                "id": [cluster_id]
            }
        }
    }

    query = f"""query GetCompliancePullTimeByCluster($filter: SnappableFilterInput,
      $first: Int = 1){{
      snappableConnection(first: $first, filter: $filter){{
        edges{{
          node{{
            pullTime
          }}
        }}
      }}
    }}"""

    return query, variables
