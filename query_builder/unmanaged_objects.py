def all_unmanaged_objects_by_cluster(cluster_id: str, after=None) -> tuple[str, dict[str, str]]:
    if after is not None:
        after_value = f'= "{after}"'
    else:
        after_value = ''

    variables = {
        "input": {
            "clusterUuid": cluster_id,
            "sortParam": {
                "sortOrder": "ASC",
                "type": "NAME"
            },
            "retentionSlaDomainIds": [],
            "objectTypes": [],
            "unmanagedStatuses": ["RELIC"]
        }
    }

    query = f"""query GetUnmanagedObjects($input: UnmanagedObjectsInput!, $first: Int = 50, $after: String {after_value}){{
      unmanagedObjects(input: $input, first: $first, after: $after){{
        edges{{
          cursor
          node{{
            id
            name
            isRemote
            localStorage
          }}
        }}
        pageInfo{{
          startCursor
          endCursor
          hasNextPage
        }}
      }}
    }}"""

    return query, variables
