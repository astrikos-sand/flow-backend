def func():
    # Implement your logic here
    import requests

    res = requests.get("http://astrikos-dev.com")
    print(res.text, flush=True)
    return res


res = func()
