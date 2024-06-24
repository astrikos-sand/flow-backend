def func(cls, params):
    # Implement your logic here
    if params is None:
        instance = cls()
    else:
        instance = cls(**params)
    return instance


instance = func(cls, params)
