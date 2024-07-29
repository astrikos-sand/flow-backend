def func(X, y, test_size, random_state):
    # Implement your logic here
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test


X_train, X_test, y_train, y_test = func(X, y, test_size, random_state)
