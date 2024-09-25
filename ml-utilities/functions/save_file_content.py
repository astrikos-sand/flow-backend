def func(name, content):
    import requests
    import io

    url = f"{_BACKEND_URL}/v2/archives/artifacts/"

    with io.BytesIO(content) as f:
        response = requests.post(
            url, files={"file": (name, f)}, data={"name": name, "flow": _FLOW_ID}
        )

        file_url = response.json()["url"]

    return file_url


file_url = func(name, content)
