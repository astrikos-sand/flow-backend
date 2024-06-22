def func():
    # Implement your logic here
    def build_regression_models_rf(
        X_train, y_train, X_test, y_test, random_state=None, param_grids=None
    ):
        from sklearn.ensemble import RandomForestRegressor
        import pandas as pd

        # Initialize an empty list to store trained models
        trained_models = []

        # If param_grids is None, build a single Random Forest model
        if param_grids is None:
            model = RandomForestRegressor(random_state=random_state)
            model.fit(X_train, y_train)
            trained_models.append(model)
        else:
            # Train Random Forest regressors for each parameter configuration
            for params in param_grids:
                # Construct the parameters dictionary with default values
                model_params = {"random_state": random_state}
                # Update the parameters with the provided values
                model_params.update(params)
                model = RandomForestRegressor(**model_params)
                model.fit(X_train, y_train)
                trained_models.append(model)

        return trained_models, X_test, y_test

    return build_regression_models_rf


build_regression_models_rf = func()
