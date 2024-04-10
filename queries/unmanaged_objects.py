def all_unmanaged_objects_by_cluster_query(cluster_id: str) -> tuple[str, dict[str,str]]:
    input_data = """
    {
      "input": {
        "clusterUuid": "{id}",
        "sortParam": {
          "sortOrder": "ASC",
          "type": "NAME"
        },
        "retentionSlaDomainIds": [],
        "objectTypes": [],
        "unmanagedStatuses": ["RELIC"]
      }
    }
    """.format(id=cluster_id)

    input_variables = {"input": input_data}

    query = """"
    query GetUnmanagedObjects($input: UnmanagedObjectsInput!){
      unmanagedObjects(input: $input){
        nodes{
          id
          name
          isRemote
          localStorage
        }
      }
    }
    """

    return query, input_variables