def func(metric_name, y_original, y_pred, args):
    # Implement your logic here
    import importlib

    module = importlib.import_module("sklearn.metrics")
    metrics = getattr(module, metric_name)
    if args is None:
        score = metrics(y_original, y_pred)
    else:
        score = metrics(y_original, y_pred, **args)
    return score


score = func(metric_name, y_original, y_pred, args)
