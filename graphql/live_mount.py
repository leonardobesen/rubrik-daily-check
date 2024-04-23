def oracle_live_mount_query() -> tuple[str, dict]:
    variables = {
        "sortBy": {
            "field": "CREATION_DATE"
        }
    }

    query = f"""query ListAllLiveMounts($sortBy: OracleLiveMountSortBy){{
      oracleLiveMounts(sortBy: $sortBy){{
        nodes{{
      		id
          sourceDatabase{{
            name
          }}
          creationDate
          cluster{{
            id
            name
          }}
        }}
      }}
    }}"""

    return query, variables


def vm_live_mount_query() -> tuple[str, dict]:
    variables = {
        "sortBy": {
            "field": "CREATION_DATE"
        }
    }

    query = f"""query ListAllLiveMounts($sortBy: VsphereLiveMountSortBy){{
      vSphereLiveMounts(sortBy: $sortBy){{
        nodes{{
      		id
          sourceVm{{
            name
          }}
          mountTimestamp
          cluster{{
            id
            name
          }}
        }}
      }}
    }}"""

    return query, variables


def mssql_live_mount_query() -> tuple[str, dict]:
    variables = {
        "sortBy": {
            "field": "CREATION_DATE"
        }
    }

    query = f"""query ListAllMssqlDbMounts($sortBy: MssqlDatabaseLiveMountSortByInput){{
      mssqlDatabaseLiveMounts(sortBy: $sortBy){{
        nodes{{
      		fid
          sourceDatabase{{
            name
          }}
          creationDate
          cluster{{
            id
            name
          }}
        }}
      }}
    }}"""

    return query, variables


def managed_volume_live_mount_query() -> tuple[str, dict]:
    variables = {
        "sortBy": "NAME"
    }

    query = f"""query ListAllManagedVolumeMounts($sortBy: HierarchySortByField){{
      managedVolumeLiveMounts(sortBy: $sortBy, sortOrder: ASC){{
        nodes{{
      	  id
          name
          channels{{
            exportDate
          }}
          cluster{{
            id
            name
          }}
        }}
      }}
    }}"""

    return query, variables
