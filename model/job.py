from services.converter import iso_to_date, miliseconds_to_duration


class Job():
    def __init__(self, id: str, object_name: str,
                 object_type: str, start_time: str,
                 duration: int, job_status: str,
                 job_type: str, sla_name: str,
                 cluster_name: str) -> None:
        self.id = id
        self.object_name = object_name
        self.object_type = object_type
        self.start_time = iso_to_date(start_time, correct_timezone=False)
        self.duration = miliseconds_to_duration(duration)
        self.job_status = job_status
        self.job_type = job_type
        self.sla_name = sla_name
        self.cluster_name = cluster_name.lower()

    def __str__(self):
        return f"""\nJob(id={self.id}, 
        object_name={self.object_name}, 
        duration={self.duration},
        cluster_name={self.cluster_name})"""
