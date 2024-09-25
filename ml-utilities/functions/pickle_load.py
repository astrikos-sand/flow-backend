def func(dumped_content):
    import pickle

    python_obj = pickle.loads(dumped_content)
    return python_obj


python_obj = func(dumped_content)
