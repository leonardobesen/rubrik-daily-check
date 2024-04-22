from model.security import ServicesAccount, SSOCertificate


def create_certificate_from_data(data):
    try:
        return SSOCertificate(
            name=data["name"],
            expiration_date=data["expirationDate"]
        )
    except Exception as e:
        print("Error processing SSO Certificate item: ", e)
        return None


def create_service_account_from_data(data):
    try:
        return ServicesAccount(
            name=data["name"],
            description=data["description"],
            last_login=data["lastLogin"]
        )
    except Exception as e:
        print("Error processing Service Account item: ", e)
        return None