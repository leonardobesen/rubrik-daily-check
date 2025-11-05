"""Module for handling job-related operations with the Rubrik API."""

import logging
from datetime import timedelta
from typing import List, Optional

from connection.wrapper import request
from model.job import Job
import graphql.jobs
from data import job_data_operation as data_operation

logger = logging.getLogger(__name__)

def get_all_jobs_above_24_hours(access_token: str) -> List[Job]:
    """
    Retrieve all jobs that have been running for more than 24 hours.

    Args:
        access_token (str): The authentication token for the Rubrik API.

    Returns:
        List[Job]: A list of Job objects representing jobs running over 24 hours.

    Raises:
        Exception: If there's an error communicating with the Rubrik API.
    """
    job_information: List[Job] = []
    above_24_hours = True
    cursor = ""

    while above_24_hours:
        try:
            query, variables = graphql.jobs.jobs_list_sort_by_duration(
                after_value=cursor
            )
            response = request(access_token, query, variables)
            
            if not response or "data" not in response:
                logger.error("Invalid response received from Rubrik API")
                break

            edges = response["data"]["reportData"]["edges"]
            if not edges:
                break

            for item in edges:
                job = _process_job_item(item)
                if not job:
                    continue

                if job.duration < timedelta(hours=24):
                    above_24_hours = False
                    break

                job_information.append(job)
                cursor = item["cursor"]

        except Exception as e:
            logger.error(f"Error fetching jobs: {str(e)}")
            raise

    return job_information

def _process_job_item(item: dict) -> Optional[Job]:
    """
    Process a single job item from the API response.

    Args:
        item (dict): The job data from the API response.

    Returns:
        Optional[Job]: A Job object if processing succeeds, None otherwise.
    """
    try:
        return data_operation.create_job_from_data(item)
    except Exception as e:
        logger.warning(f"Failed to process job item: {str(e)}")
        return None
