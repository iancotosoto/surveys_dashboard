import requests

def request_data(url: str):
    response = requests.get(url)
    return response.json()