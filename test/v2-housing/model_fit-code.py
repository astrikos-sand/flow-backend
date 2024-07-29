def func(model, x, y):
    # Implement your logic here
    model.fit(x, y)
    trained_model = model
    return trained_model


trained_model = func(model, x, y)
