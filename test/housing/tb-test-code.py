def func(tb):
    # Implement your logic here
    res = tb.model("/api/auth/user").json()
    print(res, flush=True)
    return res


res = func(tb)
