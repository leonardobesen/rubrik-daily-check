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


def all_disconnected_hosts_query(os_type: str) -> tuple[str, dict]:
    os_types = {
        "NAS": "NAS_HOST_ROOT",
        "WINDOWS": "WINDOWS_HOST_ROOT",
        "LINUX": "LINUX_HOST_ROOT",
    } 

    if os_type.upper() not in os_types.keys():
        os_type_value = os_types["NAS"]
    else:
        os_type_value = os_types[os_type]

    variables = {
        "hostRoot": os_type_value,
        "filter": [
            {
                "field": "PHYSICAL_HOST_CONNECTION_STATUS",
                "texts": [
                    "Disconnected"
                ]
            }
        ]
    }

    query = """query HostDisconnected($hostRoot:HostRoot!, $filter: [Filter!]) {
      physicalHosts(hostRoot:$hostRoot, filter:$filter) {
        nodes{
          id
          name
          connectionStatus{
            connectivity
          }
          osType
          cluster{
            id
            name
          }
        }
      }
    }"""

    return query, variables
