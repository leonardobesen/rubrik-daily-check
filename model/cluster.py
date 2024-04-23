from services.converter import iso_to_date, bytes_to_tb


class Cluster():
    def __init__(self, id: str, name: str, system_status: str,
                 pause_status: str, status: str, connected_state: str,
                 passed_connection_test: bool, last_connection_time: str,
                 total_capacity: int, used_capacity: int,
                 snapshot_capacity: int, system_capacity: int,
                 available_capacity: int, last_updated_time: str,
                 estimated_runaway: int) -> None:
        self.id = id
        self.name = name.lower()
        self.system_status = system_status
        self.pause_status = pause_status
        self.status = status
        self.connected_state = connected_state
        self.passed_connection_test = passed_connection_test
        self.last_connection_time = iso_to_date(last_connection_time)
        self.total_capacity = bytes_to_tb(total_capacity)
        self.used_capacity = bytes_to_tb(used_capacity)
        self.snapshot_capacity = bytes_to_tb(snapshot_capacity)
        self.system_capacity = bytes_to_tb(system_capacity)
        self.available_capacity = bytes_to_tb(available_capacity)
        self.last_updated_time = iso_to_date(last_updated_time)
        self.estimated_runaway = estimated_runaway
        self.in_compliance_count = 0
        self.out_of_compliance_count = 0
        self.compliance_pull_time = None

    def set_in_compliance_count(self, count: int):
        self.in_compliance_count = count

    def set_out_of_compliance_count(self, count: int):
        self.out_of_compliance_count = count

    def set_compliance_pull_time(self, iso_str: str):
        self.compliance_pull_time = iso_to_date(iso_str)

    def __str__(self):
        return f"""\nCluster(id={self.id}, 
        name={self.name}, 
        status={self.status},
        passed_connection_test={self.passed_connection_test},
        last_connection={self.last_connection_time},
        total_capacity={self.total_capacity},
        available_capacity={self.available_capacity}
        in_compliance={self.in_compliance_count},
        out_of_compliance={self.out_of_compliance_count}
        pull_time={self.compliance_pull_time})"""
