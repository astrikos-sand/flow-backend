def func(dumped_content):
    # Implement your logic here
    import pickle

    loaded_content = pickle.loads(dumped_content)
    return loaded_content


loaded_content = func(dumped_content)
