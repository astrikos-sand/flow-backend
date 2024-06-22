def func(preprocessing_dict):
    # Implement your logic here
    import pickle

    content = pickle.dumps(preprocessing_dict)
    return content


content = func(preprocessing_dict)
