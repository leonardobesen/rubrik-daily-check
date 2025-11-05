"""Job model for representing Rubrik backup jobs."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from services.converter import iso_to_date, miliseconds_to_duration


@dataclass
class Job:
    """
    Represents a Rubrik backup job.
    
    Attributes:
        id: Unique identifier for the job
        object_name: Name of the object being backed up
        object_type: Type of the object (VM, Database, etc.)
        start_time: Job start time as datetime
        duration: Job duration as timedelta
        job_status: Current status of the job
        job_type: Type of the job (Backup, Restore, etc.)
        sla_name: Name of the SLA domain
        cluster_name: Name of the Rubrik cluster
    """
    id: str
    object_name: str
    object_type: str
    start_time: datetime
    duration: timedelta
    job_status: str
    job_type: str
    sla_name: str
    cluster_name: str

    def __init__(self, id: str, object_name: str,
                 object_type: str, start_time: str,
                 duration: int, job_status: str,
                 job_type: str, sla_name: str,
                 cluster_name: str) -> None:
        """
        Initialize a Job instance.
        
        Args:
            id: Unique identifier for the job
            object_name: Name of the object being backed up
            object_type: Type of the object
            start_time: ISO format string of the start time
            duration: Duration in milliseconds
            job_status: Current status of the job
            job_type: Type of the job
            sla_name: Name of the SLA domain
            cluster_name: Name of the Rubrik cluster
        """
        self.id = id
        self.object_name = object_name
        self.object_type = object_type
        self.start_time = iso_to_date(start_time, should_fix_timezone=False)
        self.duration = miliseconds_to_duration(duration)
        self.job_status = job_status
        self.job_type = job_type
        self.sla_name = sla_name
        self.cluster_name = cluster_name.lower()

    def __str__(self) -> str:
        """Return a string representation of the Job."""
        return f"""\nJob(
            id={self.id},
            object_name={self.object_name},
            duration={self.duration},
            cluster_name={self.cluster_name}
        )"""
