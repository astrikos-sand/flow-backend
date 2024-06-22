def func(X_train, y_train, X_test, y_test, random_state, param_grids):
    # Implement your logic here
    from sklearn.ensemble import RandomForestClassifier
    import pandas as pd

    print("X_TRAIN__", X_train.shape, y_train.shape, flush=True)
    trained_models = []

    # If param_grids is None, build a single Random Forest model
    if param_grids is None:
        model = RandomForestClassifier(random_state=random_state)
        model.fit(X_train, y_train)
        trained_models.append(model)
    else:
        # Train Random Forest classifiers for each parameter configuration
        for params in param_grids:
            # Construct the parameters dictionary with default values
            model_params = {"random_state": random_state}
            # Update the parameters with the provided values
            model_params.update(params)
            print("Model trained with parameters:", model_params, flush=True)
            model = RandomForestClassifier(**model_params)
            model.fit(X_train, y_train)
            trained_models.append(model)
            print("Model trained with :", model_params, flush=True)

    X_test_ = X_test
    y_test_ = y_test
    return trained_models, X_test_, y_test_


trained_models, X_test_, y_test_ = func(
    X_train, y_train, X_test, y_test, random_state, param_grids
)
