def func(X_train, y_train, X_test, y_test, random_state, param_grids):
    # Implement your logic here
    from sklearn.ensemble import RandomForestClassifier
    import pandas as pd

    print("X_TRAIN__", X_TRAIN, flush=True)
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
            model = RandomForestClassifier(**model_params)
            model.fit(X_train, y_train)
            trained_models.append(model)
    return trained_models, X_test, y_test


trained_models, X_test, y_test = func(
    X_train, y_train, X_test, y_test, random_state, param_grids
)
