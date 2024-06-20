def func():
    # Implement your logic here
    def mode_imputation(df, columns):
        import pandas as pd
    
        if isinstance(columns, str):
            columns = [columns]
    
        # Dictionary to store median values
        mode_values = {}
    
        # Perform mode imputation
        for col in columns:
            mode_val = df[col].mode()[0]  # mode() returns a Series, so we take the first element
            df[col].fillna(mode_val, inplace=True)
            mode_values[col] = mode_val
    
        return df,mode_values

    return mode_imputation

mode_imputation = func()