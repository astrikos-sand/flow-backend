def func(python_obj):
    # Implement your logic here
    import pickle

    content = pickle.dumps(python_obj)
    return content


content = func(python_obj)
