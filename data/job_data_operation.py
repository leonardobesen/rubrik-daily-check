from model.job import Job


def create_job_from_data(data):
    try:
        if not data["node"]:
            return None

        node = data["node"]["values"]

        return Job(
            id=node[0]["displayableValue"]["stringValue"],
            object_name=node[1]["displayableValue"]["stringValue"],
            object_type=node[2]["displayableValue"]["stringValue"],
            start_time=node[3]["displayableValue"]["dateTimeValue"],
            duration=node[4]["displayableValue"]["longValue"],
            job_status=node[5]["displayableValue"]["stringValue"],
            job_type=node[6]["displayableValue"]["stringValue"],
            sla_name=node[7]["displayableValue"]["stringValue"],
            cluster_name=node[8]["displayableValue"]["stringValue"]
        )
    except Exception as e:
        print("Error processing job item: ", e)
        return None
