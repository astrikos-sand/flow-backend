import requests
import json

from config.const import WORKER_URL
from django.core.serializers.json import DjangoJSONEncoder


def submit_task(nodes: dict):
    print("nodes", nodes, flush=True)
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.post(
        WORKER_URL, data=json.dumps(nodes, cls=DjangoJSONEncoder), headers=headers
    )
    if response.status_code != 200:
        raise response.raise_for_status()
    return response.json()
