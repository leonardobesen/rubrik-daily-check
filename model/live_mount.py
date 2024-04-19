from services.converter import iso_to_date


class LiveMount():
    def __init__(self, id: str, name: str, date: str, 
                 type: str, cluster_name: str) -> None:
        self.id = id
        self.name = name
        self.date = iso_to_date(date)
        self.type = type
        self.cluster_name = cluster_name
        

    def __str__(self):
        return f"""\nLiveMount(id={self.id}, 
        name={self.name}, 
        mount_date={self.date},
        type={self.type},
        cluster={self.cluster_name})"""