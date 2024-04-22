def all_vcenters_query() -> str:
    query = f"""query ListAllVcenters {{
      vSphereVCenterConnection(sortBy:CDM_CLUSTER_NAME, sortOrder: DESC){{
        nodes{{
          name
          connectionStatus{{
            status
            message
          }}
          lastRefreshTime
          cluster{{
            id
            name
          }}
        }}
      }}
    }}"""

    return query


def all_disconnected_nas_systems_query() -> tuple[str, dict]:
    variables = {
      "hostRoot": "NAS_HOST_ROOT",
      "filter": [
        {
          "field": "PHYSICAL_HOST_CONNECTION_STATUS",
          "texts": [
            "Disconnected"
          ]
        }
      ]
    }

    query = """query NasDisconnected($hostRoot:HostRoot!, $filter: [Filter!]) {
      physicalHosts(hostRoot:$hostRoot, filter:$filter) {
        nodes{
          id
          name
          connectionStatus{
            connectivity
          }
          cluster{
            id
            name
          }
        }
      }
    }"""

    return query, variables