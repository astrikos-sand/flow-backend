def func(module_name, class_name):
    # Implement your logic here
    import importlib

    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)

    return cls


cls = func(module_name, class_name)
