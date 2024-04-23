from connection.wrapper import request
from model.security import ServicesAccount, SSOCertificate
import graphql.security
from data import security_data_operation as data_operation


def get_all_certificate_info(access_token: str) -> list[SSOCertificate]:
    certificate_information = []

    # Gather clusters information
    query = graphql.security.sso_certificate_info_query()

    try:
        response = request(access_token, query)
    except Exception:
        raise LookupError("Unable to collect certificate data!")

    if not response["data"]:
        return []

    for item in response["data"]["allCurrentOrgIdentityProviders"]:
        certificate = data_operation.create_certificate_from_data(item)
        if certificate:
            certificate_information.append(certificate)

    return certificate_information


def get_all_service_account_info(access_token: str) -> list[ServicesAccount]:
    accounts_information = []

    # Gather clusters information
    query = graphql.security.service_accounts_info_query()

    try:
        response = request(access_token, query)
    except Exception:
        raise LookupError("Unable to collect Service Accounts data!")

    if not response["data"]:
        return []

    for item in response["data"]["serviceAccounts"]["nodes"]:
        account = data_operation.create_service_account_from_data(item)
        if account:
            accounts_information.append(account)

    return accounts_information
