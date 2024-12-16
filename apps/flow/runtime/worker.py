import requests

from config.const import WORKER_URL, AIRFLOW_URL
from rest_framework.renderers import JSONRenderer


def submit_task(
    data: dict = {},
):
    json_data = JSONRenderer().render(data)

    headers = {"Content-type": "application/json", "Accept": "application/json"}

    response = requests.post(f"{WORKER_URL}/v2/", data=json_data, headers=headers)
    response.raise_for_status()
    return response.json()


def create_environment(
    data: dict = {},
):
    json_data = JSONRenderer().render(data)

    headers = {"Content-type": "application/json", "Accept": "application/json"}

    response = requests.post(
        f"{WORKER_URL}/env/",
        data=json_data,
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


def submit_notebook(
    data: dict = {},
):
    json_data = JSONRenderer().render(data)

    headers = {"Content-type": "application/json", "Accept": "application/json"}

    response = requests.post(
        f"{WORKER_URL}/notebook/start/", data=json_data, headers=headers
    )
    response.raise_for_status()
    return response.json()


def submit_dag(
    flow_id: str,
):
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.get(
        f"{AIRFLOW_URL}/dynamic-dag/create?flow={flow_id}", headers=headers
    )
    response.raise_for_status()
    return response.json()
