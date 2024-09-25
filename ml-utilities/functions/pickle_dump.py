def func(python_obj):
    import pickle

    dumped_content = pickle.dumps(python_obj)
    return dumped_content


dumped_content = func(python_obj)
