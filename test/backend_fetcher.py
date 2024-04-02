def fun(backend):
    response = backend.get("")
    return response


response = fun(backend)
