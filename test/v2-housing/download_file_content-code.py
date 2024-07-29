def func(url):
    # Implement your logic here
    import requests

    response = requests.get(url)
    content = response.content
    return content


content = func(url)
