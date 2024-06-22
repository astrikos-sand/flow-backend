def func(label_encoders, X_train_columns, best_model):
    # Implement your logic here
    preprocessing_dict = {
        "best_model": best_model,
        "X": X_train_columns,
        "label_encoders": label_encoders,
    }
    return preprocessing_dict


preprocessing_dict = func(label_encoders, X_train_columns, best_model)
