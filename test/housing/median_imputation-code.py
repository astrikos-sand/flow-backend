def func():
    # Implement your logic here
    def median_imputation(df, columns):
        import pandas as pd

        if isinstance(columns, str):
            columns = [columns]

        # Dictionary to store median values
        median_values = {}

        # Perform median imputation
        for col in columns:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            median_values[col] = median_val

        return df, median_values

    return median_imputation


median_imputation = func()
