def fun(api):
    dummy_api = api(base_url="https://dummyjson.com")
    response = dummy_api.get("/products/1")
    return response


response = fun(api)
