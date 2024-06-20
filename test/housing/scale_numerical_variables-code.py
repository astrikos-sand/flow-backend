def func():
    # Implement your logic here
    def scale_numerical_variables(df, columns=None, scaler="min-max"):
        from sklearn.preprocessing import (
            MinMaxScaler,
            StandardScaler,
            RobustScaler,
            MaxAbsScaler,
            PowerTransformer,
            QuantileTransformer,
        )
        import pandas as pd
    
        available_scalers = {
            "min-max": MinMaxScaler(),
            "standard": StandardScaler(),
            "robust": RobustScaler(),
            "max-abs": MaxAbsScaler(),
            "power": PowerTransformer(),
            "quantile": QuantileTransformer(),
        }
    
        # If no columns are specified, normalize all numerical columns
        if columns is None:
            numerical_columns = df.select_dtypes(include=["int", "float"]).columns.tolist()
        else:
            numerical_columns = columns
    
        # If no numerical columns found, return original DataFrame
        if not numerical_columns:
            print("No numerical columns found.")
            return df, {}
    
        # Check if the specified scaler is valid
        if scaler not in available_scalers:
            raise ValueError(
                f"Invalid scaler '{scaler}'. Available scalers: {', '.join(available_scalers.keys())}"
            )
    
        # Extract numerical data
        numerical_data = df[numerical_columns]
    
        # Normalize numerical columns using the specified scaler
        scaler_instance = available_scalers[scaler]
        scaled_data = scaler_instance.fit_transform(numerical_data)
    
        # Create new column names for the normalized columns
        new_column_names = [f"{col}_scaled" for col in numerical_columns]
    
        # Create a new DataFrame with the original and normalized numerical columns
        df_with_scaled = pd.DataFrame(scaled_data, columns=new_column_names, index=df.index)
    
        # Concatenate the original DataFrame with the normalized DataFrame
        df_concatenated = pd.concat([df, df_with_scaled], axis=1)
    
        # Prepare output dictionary
        output_dict = {"columns": numerical_columns, "scaler_objects": scaler_instance}
    
        return df_concatenated, output_dict

    return scale_numerical_variables

scale_numerical_variables = func()