def func(model, x, y, trained):
    # Implement your logic here
    if not trained:
        model.fit(x, y)
    else:
        model.partial_fit(x, y)

    trained_model = model
    return trained_model


trained_model = func(model, x, y, trained)
