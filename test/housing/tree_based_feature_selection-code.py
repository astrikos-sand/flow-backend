def func():
    # Implement your logic here
    def tree_based_feature_selection(df, num_features, target, task, X_columns=None):
        from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
        import pandas as pd
    
        if X_columns is None:
            X = df.drop(columns=[target])  # Assuming 'target' is the name of the target variable
        else:
            X = df[X_columns]
    
        y = df[target]
    
        # Initialize Random Forest classifier or regressor based on task
        if task == 'classification':
            rf = RandomForestClassifier()
        elif task == 'regression':
            rf = RandomForestRegressor()
        else:
            raise ValueError("Invalid task type. Task must be either 'classification' or 'regression'.")
    
        # Fit the model
        rf.fit(X, y)
    
        # Get feature importance scores
        feature_importance = rf.feature_importances_
    
        # Create a DataFrame to store feature names and their importance scores
        importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importance})
    
        # Sort features by importance score in descending order
        importance_df = importance_df.sort_values(by='Importance', ascending=False)
    
        # Select the top 'num_features' features
        top_features = importance_df.head(num_features)['Feature'].tolist()
        
        # Ensure top_features is always a list
        top_features = [top_features] if isinstance(top_features, str) else top_features
        
        # Create a dictionary with selected feature columns and target column name
        feature_info = {'top_features': top_features, 'target_column': target}
        
        # Subset the DataFrame with only the selected important features and the target column
        df_selected = df[top_features + [target]]
    
        return df_selected, feature_info

    return tree_based_feature_selection

tree_based_feature_selection = func()