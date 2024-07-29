def func(df, y_column, random_state):
    # Implement your logic here
    import pandas as pd
    from imblearn.under_sampling import RandomUnderSampler

    # Select target variable (y)
    y = df[y_column]

    # Initialize RandomUnderSampler
    sampler = RandomUnderSampler(random_state=random_state)

    # Undersample the dataset
    X_resampled, y_resampled = sampler.fit_resample(df.drop(columns=[y_column]), y)

    # Recreate DataFrame with balanced data
    balanced_df = pd.concat(
        [
            pd.DataFrame(X_resampled, columns=df.drop(columns=[y_column]).columns),
            pd.DataFrame(y_resampled, columns=[y_column]),
        ],
        axis=1,
    )
    return balanced_df


balanced_df = func(df, y_column, random_state)
