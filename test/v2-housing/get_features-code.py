def func(df, target):
    # Implement your logic here
    features = df.drop(columns=[target])
    return features


features = func(df, target)
