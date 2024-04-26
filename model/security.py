from services.converter import iso_to_date


class SSOCertificate():
    def __init__(self, name: str, expiration_date: str) -> None:
        self.name = name
        self.expiration_date = iso_to_date(expiration_date)

    def __str__(self) -> str:
        return f"""\nSSOCertificate(name={self.name}, 
        expiration_date={self.expiration_date}"""


class ServicesAccount():
    def __init__(self, name: str, description: str, last_login: str) -> None:
        self.name = name
        self.description = description
        self.last_login = iso_to_date(last_login) if last_login else None

    def __str__(self) -> str:
        return f"""\nSSOCertificate(name={self.name}, 
        expiration_date={self.description},
        last_login={self.last_login}"""
