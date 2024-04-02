import requests


def request(method: str, access_token: requests.Response, data: dict) -> requests.Response:
    base_url = 'https://totvs.my.rubrik.com/api/graphql'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    # Validate method
    valid_methods = {'GET', 'POST', 'PUT', 'PATCH', 'DELETE'}
    if method not in valid_methods:
        raise ValueError("Invalid HTTP method")

    # Use a dictionary to map methods to functions
    method_functions = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put,
        'PATCH': requests.patch,
        'DELETE': requests.delete
    }

    # Make the request
    if not data:
        response = method_functions[method](base_url, headers=headers)
    else:
        response = method_functions[method](base_url, data=data, headers=headers)

    return response
