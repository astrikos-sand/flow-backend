def func(params):
    # Implement your logic here
    from sklearn.ensemble import RandomForestClassifier

    if params is None:
        model = RandomForestClassifier()
    else:
        model = RandomForestClassifier(**params)
    return model


model = func(params)
