def func():
    # Implement your logic here
    def predict(preprocessing_dict, new_df):
        import pandas as pd
        import numpy as np
    
        X = None

        for step, parameters in preprocessing_dict.items():
            print(f"Processing step: {step}", flush=True)
            if step == 'mean_imputation':
                # Perform mean imputation on specified numerical columns
                for column, mean_value in parameters.items():
                    new_df[column].fillna(mean_value, inplace=True)
            
            elif step == 'median_imputation':
                # Perform median imputation on specified numerical columns
                for column, median_value in parameters.items():
                    new_df[column].fillna(median_value, inplace=True)
            
            elif step == 'mode_imputation':
                # Perform mode imputation on specified categorical columns
                for column, mode_value in parameters.items():
                    new_df[column].fillna(mode_value, inplace=True)
                    
            elif step == 'anomalies_info':
                #get columns
                columns = list(parameters.get('columnX'))
                model = parameters.get('model')
                
                X = new_df[columns]
                
                # Predict outliers
                new_df['anomaly'] = model.predict(X)
                new_df['anomaly'] = new_df['anomaly'].map({1: 0, -1: 1})
                
            elif step == 'tree_based_feature_selection':
                #get columns
                columnX = list(parameters.get('top_features'))
                columnY = parameters.get('target_column')
                
                new_df = new_df[columnX + [columnY]]
                
            elif step == 'pca_based_feature_selection':
                # Get columns
                columns_used = parameters.get('columns_used')
                target_column = parameters.get('target_column')
                # Get trained PCA model
                pca_object = parameters.get('pca_object')
    
                # Separate features (X) and target variable (y)
                X = new_df[columns_used]
                y = new_df[target_column]
    
                # Transform the data
                X_reduced = pca_object.transform(X)
    
                # Create a DataFrame with the reduced dimensionality
                pca_column_names = [f'PC{i}' for i in range(1, X_reduced.shape[1] + 1)]
                df_reduced = pd.DataFrame(X_reduced, columns=pca_column_names)
    
                # Add non-PCA columns and the target variable back to the DataFrame
                non_pca_columns = [col for col in new_df.columns if col not in columns_used]
                for col in non_pca_columns:
                    df_reduced[col] = new_df[col]
                df_reduced[target_column] = y
    
                new_df = df_reduced
                    
            elif step == 'bin_numerical_features':
                
                binning_info = parameters
                for col, info in binning_info.items():
                    bin_size = info['bin_size']
                    bins_range = info['bin_ranges']
                    bin_labels = [f"{start}-{end}" for start, end in bins_range]
    
                    # Check if any value in the column falls outside the specified bin ranges
                    if new_df[col].min() < bins_range[0][0] or new_df[col].max() > bins_range[-1][1]:
                        print(f"Warning: Value(s) in column '{col}' are out of bin range.")
                        print('Execution stopped')
                        break
    
                    new_df[f"{col}_grouped_{bin_size}_bins"] = pd.cut(new_df[col], bins=[start for start, end in bins_range] + [info['max']+1], labels=bin_labels, include_lowest=True)
        
            elif step == 'impute_missing_values_with_rfg':
                
                break_loop = False
                
                # Fill mean and mode values for columnx
                col_mean = parameters.get('column_x_mean', {})
                for col, value in col_mean.items():
                    new_df[col].fillna(value, inplace=True)
                
                col_mode = parameters.get('column_x_mode', {})
                for col, value in col_mode.items():
                    new_df[col].fillna(value, inplace=True)
                
                # Transform categorical data using encoders
                encoders = parameters.get('encoders', {})
                for col, encoder in encoders.items():
                    if col in new_df.columns:
                        try:
                            new_df[col] = encoder.transform(new_df[col])
                        except:
                            print("Warning: New label found in column :", col)
                            break_loop = True
                            break        
                if break_loop:
                    print('execution has been stopped, please opt for mode Train')
                    break   
                        
                # Get the trained Random Forest classifier
                rf_regressor = parameters.get('rf_regressor')
                
                # Predict missing values
                y_column = parameters.get('column_y', None)
                if y_column and new_df[y_column].isnull().all():
                    X_columns = preprocessing_dict['impute_missing_values_with_rfg']['X_train_flow']
                    X_missing = new_df[new_df[y_column].isnull()][X_columns]
                    y_missing_predicted = rf_regressor.predict(X_missing)
                    # Impute missing values in original DataFrame
                    new_df.loc[new_df[y_column].isnull(), y_column] = y_missing_predicted
                    for col, encoder in encoders.items():
                        if col in new_df.columns:
                            new_df[col] = encoder.inverse_transform(new_df[col]) 
                else:
                    for col, encoder in encoders.items():
                        if col in new_df.columns:
                            new_df[col] = encoder.inverse_transform(new_df[col])
                    
            elif step == 'impute_missing_values_with_rfc':
                
                break_loop = False
                
                # Fill mean and mode values for columnx
                col_mean = parameters.get('column_x_mean', {})
                for col, value in col_mean.items():
                    new_df[col].fillna(value, inplace=True)
                
                col_mode = parameters.get('column_x_mode', {})
                for col, value in col_mode.items():
                    new_df[col].fillna(value, inplace=True)
                
                # Transform categorical data using encoders
                encoders = parameters.get('encoders', {})
                for col, encoder in encoders.items():
                    if col in new_df.columns:
                        try:
                            new_df[col] = encoder.transform(new_df[col])
                        except:
                            print("Warning: New label found in column :", col)
                            break_loop = True
                            break       
                if break_loop:
                    print('execution has been stopped, please opt for mode Train')
                    break   
                        
                # Get the trained Random Forest classifier
                rf_classifier = parameters.get('rf_classifier')
                
                # Predict missing values
                y_column = parameters.get('column_y', None)
                if y_column and new_df[y_column].isnull().all():
                    X_columns = preprocessing_dict['impute_missing_values_with_rfc']['X_train_flow']
                    X_missing = new_df[new_df[y_column].isnull()][X_columns]
                    y_missing_predicted = rf_classifier.predict(X_missing)
                    # Impute missing values in original DataFrame
                    new_df.loc[new_df[y_column].isnull(), y_column] = y_missing_predicted
                    for col, encoder in encoders.items():
                        if col in new_df.columns:
                            new_df[col] = encoder.inverse_transform(new_df[col])
                else:
                    for col, encoder in encoders.items():
                        if col in new_df.columns:
                            new_df[col] = encoder.inverse_transform(new_df[col])
                    
            elif step == 'iterative_imputation':
                
                # Encode categorical variables
                categorical_info = preprocessing_dict.get('iterative_imputation', {}).get('categorical', None)
                numerical_info = preprocessing_dict.get('iterative_imputation', {}).get('numerical', None)
    
                if categorical_info:
    
                    categorical_encoder = categorical_info.get('encoder', {})
                    categorical_columns = categorical_info.get('columns', [])
    
                    # Flag variable to break the loop
                    break_loop = False
    
                    for col in categorical_columns:
                        encoder = categorical_encoder.get(col)
                        if encoder is None:
                            continue
    
                        col_values = new_df[col].tolist()
    
                        # Remove np.nan and None from the list and remember their positions
                        indices_to_remove = [i for i, x in enumerate(col_values) if (isinstance(x, (int, float)) and np.isnan(x)) or x is None]
                        values_to_add_back = [x for x in col_values if (isinstance(x, (int, float)) and np.isnan(x)) or x is None]
                        col_values = [x for x in col_values if not (isinstance(x, (int, float)) and np.isnan(x)) and x is not None]
    
                        try:
                            # Transform the modified list using the encoder
                            new_col_values = list(encoder.transform(col_values))
                        except:
                            # Handle the case where a new label appears
                            print("Warning: New label found in column :", col)
                            break_loop = True
                            break
    
    
                        # Add np.nan and None back to their original positions in the new_col_values
                        for index, value in zip(indices_to_remove, values_to_add_back):
                            new_col_values.insert(index, value)
    
                        # Replace the col values with the new list
                        new_df[col] = new_col_values
    
                    if break_loop:
                        print('execution has been stopped, please opt for mode Train')
                        break
    
                if numerical_info:
                    # Impute missing values for numerical columns
                    numerical_columns = numerical_info.get('columns', [])
                    numerical_imputer = numerical_info.get('model', None)
    
                    if numerical_imputer:
                        new_df[numerical_columns] = numerical_imputer.transform(new_df[numerical_columns])
    
                if categorical_info:
                    # Impute missing values for categorical columns
                    categorical_imputer = categorical_info.get('model', None)
                    if categorical_imputer:
                        new_df[categorical_columns] = categorical_imputer.transform(new_df[categorical_columns])
    
                    # Decode categorical variables
                    for col in categorical_columns:
                        encoder = categorical_encoder.get(col)
                        if encoder:
                            encoded_list = new_df[col].astype(int).tolist()
                            decoded_list = encoder.inverse_transform(encoded_list)
                            new_df[col] = decoded_list
    
                
            # elif step == 'columns_to_delete':
            #     columns_to_delete = parameters
            #     new_df = delete_columns(new_df, columns_to_delete)
            
            # elif step == 'rows_to_delete':
            #     params = parameters
            #     input_params = [new_df] + params
            #     new_df = delete_rows(*input_params)
                
            # elif step == 'delete_rows_using_colvalues':
            #     params = parameters
            #     input_params = [new_df] + params
            #     new_df = row_deletion_using_colvalues(*input_params)
                 
            elif step == 'label_encoders':
                label_encoders = parameters
                for column, encoder in label_encoders.items():
                    if column in new_df.columns:
                        new_df[column+ '_encoded'] = encoder.transform(new_df[[column]])
                        
            elif step == 'normalized_features':
                columns = parameters.get('columns')
                scaler = parameters.get('scaler_objects')
                
                numerical_data = new_df[columns]
                
                scaled_data = scaler.transform(numerical_data)
                # Create new column names for the normalized columns
                new_column_names = [f"{col}_scaled" for col in columns]
                
                # Create a new DataFrame with the original and normalized numerical columns
                df_with_scaled = pd.DataFrame(scaled_data, columns=new_column_names, index=new_df.index)
                
                # Concatenate the original DataFrame with the normalized DataFrame
                new_df = pd.concat([new_df, df_with_scaled], axis=1)
                    
                        
            elif step == 'X':
                X_cols = parameters
                X = new_df[X_cols]
                
            elif step == 'best_model':
                best_model = parameters
                if X is not None:
                    predictions = best_model.predict(X)
                    new_df['predicted_values'] = predictions
                else:
                    print("Error: 'X' variables not found.")
            else:
                print(f"Warning: Unknown preprocessing step '{step}'. Skipping...")
    
        return new_df

    return predict

predict = func()