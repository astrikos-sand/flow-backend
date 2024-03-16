import requests
import json

from config.const import WORKER_URL
from django.core.serializers.json import DjangoJSONEncoder

# type = "Normal" | "Triggered"


def submit_task(
    nodes: dict, data: dict = {}, type: str = "Normal", trigger_id: str = None
):

    if type == "Triggered" and trigger_id is None:
        raise Exception("When task type is triggred then trigger_id is required")

    print("nodes", nodes, flush=True)
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    data = {"nodes": nodes, "data": data, "type": type}
    response = requests.post(
        WORKER_URL, data=json.dumps(data, cls=DjangoJSONEncoder), headers=headers
    )
    if response.status_code != 200:
        raise response.raise_for_status()
    return response.json()
