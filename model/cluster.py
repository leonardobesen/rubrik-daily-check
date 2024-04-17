from datetime import datetime

class Cluster():
    def __init__(self, id: str, name: str, system_status: str, 
                 pause_status: str, status: str, connected_state: str,
                 is_connection_checked: bool, last_connection_time: str, 
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
        self.is_connection_checked = is_connection_checked
        self.last_connection_time = self.iso_to_date(last_connection_time)
        self.total_capacity = self.bytes_to_tb(total_capacity)
        self.used_capacity = self.bytes_to_tb(used_capacity)
        self.snapshot_capacity = self.bytes_to_tb(snapshot_capacity)
        self.system_capacity = self.bytes_to_tb(system_capacity)
        self.available_capacity = self.bytes_to_tb(available_capacity)
        self.last_updated_time = self.iso_to_date(last_updated_time)
        self.estimated_runaway = estimated_runaway
        self.in_compliance_count = None
        self.out_of_compliance_count = None
        self.compliance_pull_time = None

    def set_in_compliance_count(self, count: int):
        self.in_compliance_count = count
    
    def set_out_of_compliance_count(self, count: int):
        self.out_of_compliance_count = count

    def set_compliance_pull_time(self, iso_str: str):
        try:
            date_obj = datetime.fromisoformat(iso_str)
            self.compliance_pull_time = date_obj
        except ValueError:
            print(f"Invalid ISO8601 format provided for compliance on {self.name}")
            self.compliance_pull_time = None
        
    
    def iso_to_date(self, iso_str: str):
        try:
            date_obj = datetime.fromisoformat(iso_str)
            return date_obj
        except ValueError:
            print(f"Invalid ISO8601 format provided for {self.name}")
            return None
    
    def bytes_to_tb(self, bytes_size: int):
        return round(bytes_size/(1000**4), 2)

    def __str__(self):
        return f"""\nCluster(id={self.id}, 
        name={self.name}, 
        status={self.status},
        is_connected={self.is_connection_checked},
        last_connection={self.last_connection_time},
        total_capacity={self.total_capacity},
        available_capacity={self.available_capacity}
        in_compliance={self.in_compliance_count},
        out_of_compliance={self.out_of_compliance_count}
        pull_time={self.compliance_pull_time})"""
       
        
        