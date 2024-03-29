def fun(backend):
    response = backend.get("")
    return response


result = fun(backend)
