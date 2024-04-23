from services.converter import iso_to_date


class VCenter():
    def __init__(self, name: str, status: str, status_message: str,
                 last_refresh_time: str, cluster_name: str) -> None:
        self.name = name
        self.status = status
        self.status_message = status_message
        self.last_refresh_time = iso_to_date(last_refresh_time)
        self.cluster_name = cluster_name.lower()

    def __str__(self):
        return f"""\nVCenter(name={self.name}, 
        status={self.status}, 
        status_message={self.status_message},
        last_refresh_time={self.last_refresh_time},
        cluster={self.cluster_name})"""


class Nas():
    def __init__(self, id: str, name: str,
                 connection_status: str, cluster_name: str) -> None:
        self.id = id
        self.name = name
        self.connection_status = connection_status
        self.cluster_name = cluster_name.lower()

    def __str__(self):
        return f"""\nVCenter(id={self.id}, 
        name={self.name}, 
        connection_status={self.connection_status},
        cluster_name={self.cluster_name})"""
