def all_cluster_info_query() -> tuple[str, dict]:
    variables = {
        "filter": {
            "productFilters": [
                {
                    "productType": "CDM"
                }
            ]
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


def all_clusters_compliance():
    variables = {
        "primaryGroupBy": "ComplianceStatus",
        "secondaryGroupBy": "Cluster",
        "filter": {
            "complianceStatus": ["IN_COMPLIANCE", "OUT_OF_COMPLIANCE"],
            "protectionStatus": [],
            "slaTimeRange": "LAST_24_HOURS",
            "orgId": []
        }
    }

    query = f"""query GetClustersCompliance($primaryGroupBy: SnappableGroupByEnum!, 
      $secondaryGroupBy: SnappableGroupByEnum!, 
      $filter: SnappableGroupByFilterInput) {{
      snappableGroupByConnection(groupBy: $primaryGroupBy, 
        filter: $filter) {{
        nodes {{
          groupByInfo {{
            ... on ComplianceStatus {{
              ComplianceStatus: enumValue
            }}
          }}
          clusterGroup: snappableGroupBy(groupBy: $secondaryGroupBy) {{
            clusterInfo: groupByInfo {{
              ... on Cluster {{
                clusterName: name
              }}
            }}
            complianceCount: snappableConnection {{
              count
            }}
          }}
        }}
      }}
    }}"""

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
