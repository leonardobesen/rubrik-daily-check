from connection.wrapper import request
from model.job import Job
import graphql.jobs
from data import job_data_operation as data_operation
from datetime import timedelta


def get_all_jobs_above_24_hours(access_token: str) -> list[Job]:
    job_information = []
    above_24_hours = True
    cursor = ""

    while above_24_hours:
        query, variables = graphql.jobs.jobs_list_sort_by_duration(
            after_value=cursor)

        try:
            response = request(access_token, query, variables)
        except:
            response["data"] = None

        if not response["data"]:
            above_24_hours = False
            continue

        for item in response["data"]["reportData"]["edges"]:
            job = data_operation.create_job_from_data(item)
            if not job:
                continue

            if job.duration < timedelta(hours=24):
                above_24_hours = False
                break

            job_information.append(job)
            cursor = item["cursor"]

    return job_information
