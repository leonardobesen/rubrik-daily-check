def jobs_list_sort_by_duration(after_value = None) -> tuple[str, dict]:
    if after_value:
        after_string = f"=  {after_value}"
    else:
        after_string = ""

    variables = {
      "dataView": "MONITORING_IN_PROGRESS",
      "filters": [
        {
          "name": "job_type",
          "values": [
            "Backup",
            "Log Backup"
          ]
        }
      ],
      "columns": [
        "event_series_id",
        "start_time",
        "duration",
        "job_status",
        "job_type",
        "object_type",
        "object_name",
        "sla_domain_name",
        "cluster_name"
      ],
      "sortBy": "start_time",
      "sortOrder": "ASC",
      "timezone": "America/Sao_Paulo",
      "first": 100
    }

    query = f"""query EventsRunningForMoreThan24Hours(
      $dataView: DataViewTypeEnum!, 
      $filters: [ReportFilterInput!],
      $columns: [String!]!, 
      $sortBy: String, 
      $sortOrder: SortOrder,
      $first: Int, 
      $after: String {after_string}, 
      $timezone: String) {{
    	reportData(dataView: $dataView, 
        columns: $columns, 
        filters: $filters,
        sortBy: $sortBy, 
        sortOrder: $sortOrder,
        first: $first, 
        after: $after, 
        timezone: $timezone) {{
        edges {{
          node {{
            values {{
              displayableValue {{
                displayValue
                ... on DisplayableValueBoolean {{
                  booleanValue: value
                }}
                ... on DisplayableValueFloat {{
                  floatValue: value
                }}
                ... on DisplayableValueInteger {{
                  intValue: value
                }}
                ... on DisplayableValueLong {{
                  longValue: value
                }}
                ... on DisplayableValueString {{
                  stringValue: value
                }}
                ... on DisplayableValueDateTime {{
                  dateTimeValue: value
                }}
              }}
            }}
          }}
        }}
        pageInfo {{
          endCursor
          hasNextPage
          hasPreviousPage
        }}
      }}
    }}"""

    return query, variables