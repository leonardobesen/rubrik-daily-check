def sso_certificate_info_query() -> str:
    query = """query SingleSignOnCertificates {
      allCurrentOrgIdentityProviders {
        name
        expirationDate
      }
    }"""

    return query


def service_accounts_info_query() -> str:
    query = """query GetServiceAccounts {
      serviceAccounts {
        nodes {
          name
          description
          lastLogin
        }
      }
    }
    """

    return query