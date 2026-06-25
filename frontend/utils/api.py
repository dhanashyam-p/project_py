import requests
from frontend.config import BACKEND_URL


def api_get(endpoint, token=None):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(
        f"{BACKEND_URL}{endpoint}",
        headers=headers,
        timeout=30,
    )
    return response


def api_post(endpoint, data, token=None):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.post(
        f"{BACKEND_URL}{endpoint}",
        json=data,
        headers=headers,
        timeout=30,
    )
    return response


def api_put(endpoint, data, token=None):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.put(
        f"{BACKEND_URL}{endpoint}",
        json=data,
        headers=headers,
        timeout=30,
    )
    return response


def api_delete(endpoint, token=None):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.delete(
        f"{BACKEND_URL}{endpoint}",
        headers=headers,
        timeout=30,
    )
    return response