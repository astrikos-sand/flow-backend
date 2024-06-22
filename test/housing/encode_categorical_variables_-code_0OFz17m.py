def func(df, columns):
    # Implement your logic here
    from sklearn.preprocessing import LabelEncoder

    if columns is None:
        categorical_columns = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()
    else:
        categorical_columns = columns

    # If no categorical columns found, return original DataFrame
    if not categorical_columns:
        return df, {}

    # Perform label encoding for each categorical column
    label_encoders = {}
    for col in categorical_columns:
        label_encoders[col] = LabelEncoder()
        df[col + "_encoded"] = label_encoders[col].fit_transform(df[col])

    new_df = df
    return new_df, label_encoders


new_df, label_encoders = func(df, columns)
