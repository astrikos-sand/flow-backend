def func():
    # Implement your logic here
    def pca_based_feature_selection(df, num_components, target, columns_X=None):
        from sklearn.decomposition import PCA
        import pandas as pd

        # Select columns for PCA
        if columns_X is None:
            X = df.drop(columns=[target])  # Assume all columns except the target
            columns_used = list(X.columns)
        else:
            X = df[columns_X]
            columns_used = columns_X

        # Separate target variable (y)
        y = df[target]

        # Initialize PCA
        pca = PCA(n_components=num_components)

        # Fit and transform the data
        X_reduced = pca.fit_transform(X)

        # Create a DataFrame with the reduced dimensionality
        pca_column_names = [f"PC{i}" for i in range(1, num_components + 1)]
        df_reduced = pd.DataFrame(X_reduced, columns=pca_column_names)

        # Add non-PCA columns and the target variable back to the DataFrame
        non_pca_columns = [col for col in df.columns if col not in columns_used]
        for col in non_pca_columns:
            df_reduced[col] = df[col]
        df_reduced[target] = y

        # Create pca_info dictionary
        pca_info = {
            "pca_object": pca,
            "columns_used": columns_used,
            "target_column": target,
        }

        return df_reduced, pca_info

    return pca_based_feature_selection


pca_based_feature_selection = func()
