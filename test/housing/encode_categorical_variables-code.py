def func():
    # Implement your logic here
    def encode_categorical_variables(df, columns=None):
        from sklearn.preprocessing import LabelEncoder
        import pandas as pd
        # If no columns are specified, identify categorical columns
        if columns is None:
            categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        else:
            categorical_columns = columns
        
        # If no categorical columns found, return original DataFrame
        if not categorical_columns:
            return df, {}
        
        # Perform label encoding for each categorical column
        label_encoders = {}
        for col in categorical_columns:
            label_encoders[col] = LabelEncoder()
            df[col + '_encoded'] = label_encoders[col].fit_transform(df[col])
        
        return df,label_encoders

    return encode_categorical_variables

encode_categorical_variables = func()