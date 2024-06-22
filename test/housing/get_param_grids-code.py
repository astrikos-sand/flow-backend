def func():
    # Implement your logic here
    param_grids = [
        {
            "n_estimators": 200,
            "max_depth": 10,
            "min_samples_split": 5,
            "min_samples_leaf": 2,
            "max_features": "log2",
            "bootstrap": True,
        },
        {
            "n_estimators": 300,
            "max_depth": 20,
            "min_samples_split": 10,
            "min_samples_leaf": 4,
            "max_features": "sqrt",
            "bootstrap": True,
        },
        {
            "n_estimators": 400,
            "max_depth": 30,
            "min_samples_split": 15,
            "min_samples_leaf": 6,
            "max_features": 0.5,
            "bootstrap": False,
        },
    ]
    return param_grids


param_grids = func()
