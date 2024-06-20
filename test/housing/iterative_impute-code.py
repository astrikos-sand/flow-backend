def func():
    # Implement your logic here
    def iterative_impute(df, columns=None):
        import pandas as pd
        from sklearn.preprocessing import LabelEncoder
        from sklearn.experimental import enable_iterative_imputer  
        from sklearn.impute import IterativeImputer
        from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
    
        if columns is None:
            categorical_cols = [[col] for col in df.select_dtypes(include=['object']).columns.tolist()]
            categorical = df.select_dtypes(include=['object']).columns.tolist()
            numerical = df.select_dtypes(include=['number']).columns.tolist()
        else:
            categorical_cols = [[col] for col in columns['categorical']]
            categorical = columns['categorical']
            numerical = columns['numerical']
    
    
        # Encode categorical variables using LabelEncoder
        label_encoders = {}
        for col in categorical_cols:
            encoder = LabelEncoder()
            df[col] = df[col].apply(lambda series: pd.Series(
                encoder.fit_transform(series[series.notnull()]),
                index=series[series.notnull()].index
            ))
            label_encoders[col[0]] = encoder
    
        # Impute missing values
        imputation_models = {}
        if numerical:
            imp_num = IterativeImputer(estimator=RandomForestRegressor(),
                                       initial_strategy='mean',
                                       max_iter=100, random_state=0)
            df[numerical] = imp_num.fit_transform(df[numerical])
            imputation_models['numerical'] = {'columns': numerical, 'model': imp_num}
    
        if categorical:
            imp_cat = IterativeImputer(estimator=RandomForestClassifier(), 
                                       initial_strategy='most_frequent',
                                       max_iter=100, random_state=0)
            df[categorical] = imp_cat.fit_transform(df[categorical])
            imputation_models['categorical'] = {'columns': categorical, 'model': imp_cat, 'encoder': label_encoders}
    
        # Decode categorical variables
        for col in categorical_cols:
            encoder = label_encoders[col[0]]
            df[col] = df[col].apply(lambda series: pd.Series(
                encoder.inverse_transform(series.astype(int)),
                index=series.index
            ))
    
        return df, imputation_models


    return iterative_impute

iterative_impute = func()