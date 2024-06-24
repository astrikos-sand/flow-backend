def func(url):
    # Implement your logic here
    print("***********dfnkdnfsdkf**************", flush=True)
    print(url, flush=True)
    import requests

    response = requests.get(url)
    content = response.content
    return content


content = func(url)
