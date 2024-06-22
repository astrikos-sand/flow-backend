def func():
    # Implement your logic here
    def mean_imputation(df, columns):
        import pandas as pd

        if isinstance(columns, str):
            columns = [columns]

        # Dictionary to store mean values
        mean_values = {}

        # Perform mean imputation
        for col in columns:
            mean_val = df[col].mean()
            df[col].fillna(mean_val, inplace=True)
            mean_values[col] = mean_val

        return df, mean_values

    return mean_imputation


mean_imputation = func()
