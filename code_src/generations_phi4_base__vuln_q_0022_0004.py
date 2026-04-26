import requests

def update_account_settings(url, data):
    response = requests.post(url, data=data)
    return response.status_code, response.json()