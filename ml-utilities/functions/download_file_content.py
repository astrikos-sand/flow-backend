def func(url):
    import requests

    response = requests.get(url)
    content = response.content
    return content


content = func(url)
