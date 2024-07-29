def func(key, content, url):
    import requests

    # Implement your logic here
    with open(key, "wb") as f:
        f.write(content)

    with open(key, "rb") as f:
        files = {"file": (key, f)}
        res = requests.post(url, files=files, data={"name": key})
        print(res.text)
    return


func(key, content, url)
