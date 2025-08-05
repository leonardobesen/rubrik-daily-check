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


def all_disconnected_hosts_query(os_type: str, after_value="") -> tuple[str, dict]:
    if after_value:
        after_string = f" = {after_value}"
    else:
        after_string = ""

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
          "field": "CLUSTER_ID",
          "texts": [
            "ebc3f3ed-7981-4b77-a5e0-efe3ce3f48b3"
          ]
        },
        {
          "field": "IS_RELIC",
          "texts": [
            "false"
          ]
        },
        {
          "field": "IS_REPLICATED",
          "texts": [
            "false"
          ]
        },
        {
          "field": "PHYSICAL_HOST_CONNECTION_STATUS",
          "texts": [
            "Disconnected"
          ]
        },
        {
          "field": "IS_KUPR_HOST",
          "texts": [
            "false"
          ]
        }
      ],
      "sortBy": "NAME",
      "sortOrder": "ASC"
    }

    query = f"""query HostDisconnected(
      $hostRoot:HostRoot!, 
      $filter: [Filter!],
      $after: String {after_string}) {{
      physicalHosts(
        hostRoot:$hostRoot, 
        filter:$filter) {{
        pageInfo {{
          hasNextPage
          endCursor      
        }}
        nodes{{
          id
          name
          connectionStatus{{
            connectivity
          }}
          osType
          cluster{{
            id
            name
          }}
        }}
      }}
    }}"""

    return query, variables
