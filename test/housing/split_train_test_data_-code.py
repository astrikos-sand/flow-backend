def func(df, target, X_variables, test_size, random_state, sampling, type):
    # Implement your logic here
    from sklearn.model_selection import train_test_split
    import pandas as pd
    from imblearn.over_sampling import SMOTE

    print("Splitting the data into training and testing sets...", flush=True)

    if X_variables:
        # Update the DataFrame to include only the specified features and the target variable
        columns_to_keep = [target] + X_variables
        df = df[columns_to_keep]

    if type == "classification":
        if sampling == "undersampling":
            # Undersampling strategy
            df_undersampled = undersample_df(df, target, random_state=random_state)
            X_undersampled = df_undersampled.drop(columns=[target])
            y_undersampled = df_undersampled[target]

            # Split the undersampled dataset into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(
                X_undersampled,
                y_undersampled,
                test_size=test_size,
                random_state=random_state,
            )

            return X_train, X_test, y_train, y_test

        elif sampling == "oversampling":

            # Oversampling strategy
            X = df.drop(columns=[target])
            y = df[target]

            # Split the original dataset into training and testing sets
            X_train_full, X_test, y_train_full, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )

            # Concatenate the training features and target variable for oversampling
            train_df_full = pd.concat([X_train_full, y_train_full], axis=1)

            try:
                # Oversample the training data
                X_train_oversampled, y_train_oversampled = oversampling(
                    train_df_full, target, random_state=random_state
                )
                return X_train_oversampled, X_test, y_train_oversampled, y_test
            except ValueError as e:
                print(
                    "Samples in minority class are too few to oversample. Continueing with the train-test split "
                )
                return X_train_full, X_test, y_train_full, y_test

        elif sampling is None:
            # No sampling strategy specified
            X = df.drop(columns=[target])
            y = df[target]

            # Split the dataset into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )
            return X_train, X_test, y_train, y_test

    else:
        # For regression or any other task type
        X = df.drop(columns=[target])
        y = df[target]

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
    return X_train, X_test, y_train, y_test


X_train, X_test, y_train, y_test = func(
    df, target, X_variables, test_size, random_state, sampling, type
)
