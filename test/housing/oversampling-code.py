def func():
    # Implement your logic here
    def oversampling(df, y, random_state=None):
        # Set random seed if provided
        import pandas as pd
        from imblearn.over_sampling import SMOTE, SMOTENC
        import random

        if random_state is not None:
            random.seed(random_state)

        # Separate features (X_train) and target variable (y_train)
        X_train = df.drop(columns=[y])
        y_train = df[y]

        # Check if all columns in X_train are categorical
        if all(X_train[col].dtype == "object" for col in X_train.columns):

            target_ratio = 1.0

            # Count the number of samples in each class
            class_counts = y_train.value_counts()

            # Find the majority and minority classes
            majority_class = class_counts.idxmax()
            minority_class = class_counts.idxmin()

            # Determine the number of samples needed to reach the target ratio
            target_count = (
                int(class_counts[majority_class] * target_ratio)
                - class_counts[minority_class]
            )

            # Get indices of minority class samples
            minority_indices = y_train[y_train == minority_class].index.tolist()

            # Randomly oversample minority class samples
            oversampled_indices = random.choices(minority_indices, k=target_count)

            # Get the oversampled minority class samples
            oversampled_samples = df.loc[oversampled_indices]

            # Concatenate the original majority class samples with the randomly oversampled minority class samples
            df_resampled = pd.concat([df, oversampled_samples])

            X_resampled = df_resampled.drop(columns=[y])
            y_resampled = df_resampled[y]

            return X_resampled, y_resampled

        # Check if all columns in X_train are numerical
        if all(X_train[col].dtype != "object" for col in X_train.columns):

            # Create SMOTE sampler for numerical features
            smote = SMOTE(random_state=random_state)
            X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
        else:
            # Find categorical features indices
            categorical_features_indices = [
                i
                for i, col in enumerate(X_train.columns)
                if X_train[col].dtype == "object"
            ]

            # Create SMOTENC sampler for mixed data
            smote_nc = SMOTENC(
                categorical_features=categorical_features_indices,
                random_state=random_state,
            )
            X_resampled, y_resampled = smote_nc.fit_resample(X_train, y_train)

        return X_resampled, y_resampled

    return oversampling


oversampling = func()
