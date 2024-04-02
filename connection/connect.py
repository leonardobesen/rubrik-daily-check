import requests
import json


def open_session(CONFIG_FILE: str) -> requests.Response:
    with open(CONFIG_FILE, 'r') as json_file:
        config = json.load(json_file)

    headers = {'Content-Type': 'application/json'}

    data = {
        'client_id': config["client_id"],
        'client_secret': config["client_secret"]
    }

    access_token = requests.post(
        'https://totvs.my.rubrik.com/api/client_token', data=data, headers=headers)

    return access_token


def close_session(access_token: requests.Response):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    requests.delete(
        'https://totvs.my.rubrik.com/api/client_token', headers=headers)
