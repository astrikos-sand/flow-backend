import requests
import json
from enum import auto
from strenum import StrEnum

from config.const import WORKER_URL
from django.core.serializers.json import DjangoJSONEncoder


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
