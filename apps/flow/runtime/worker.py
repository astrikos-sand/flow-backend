import requests
import json
from enum import auto
from strenum import StrEnum

from config.const import WORKER_URL
from django.core.serializers.json import DjangoJSONEncoder

from apps.flow.serializers import NodeResultSerializer


# type = "Normal" | "Triggered"


class SUBMIT_TASK_TYPE(StrEnum):
    NORMAL = "NORMAL"
    TRIGGERED = "TRIGGERED"


def submit_task(
    nodes: dict,
    data: dict = {},
    type: SUBMIT_TASK_TYPE = SUBMIT_TASK_TYPE.NORMAL,
    trigger_node: str = None,
):

    if type == SUBMIT_TASK_TYPE.TRIGGERED and trigger_node is None:
        raise Exception("When task type is triggred then trigger_node is required")

    headers = {"Content-type": "application/json", "Accept": "application/json"}
    data = {"nodes": nodes, "data": data, "trigger_node": trigger_node, "type": type}
    response = requests.post(
        WORKER_URL, data=json.dumps(data, cls=DjangoJSONEncoder), headers=headers
    )
    response.raise_for_status()
    return response.json()


def save_results(results: dict):
    for node_id in results:
        res = results[node_id]
        data = {
            "node": node_id,
            "outputs": res.get("outputs", {}),
            "inputs": res.get("inputs", {}),
        }
        serializer = NodeResultSerializer(data=data)
        if serializer.is_valid():
            serializer.save()


def create_environment(requirements: str, id: str):
    data = {"requirements": requirements, "id": id}
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.post(
        f"{WORKER_URL}/env/",
        data=json.dumps(data, cls=DjangoJSONEncoder),
        headers=headers,
    )
    response.raise_for_status()
    return response.json()
