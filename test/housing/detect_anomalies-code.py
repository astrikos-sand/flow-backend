def func():
    # Implement your logic here

    def detect_anomalies(df, contamination_factor, columns=None):
        import pandas as pd
        from sklearn.ensemble import IsolationForest

        if columns is None:
            X = df
        else:
            X = df[columns]

        columnX = X.columns

        # Initialize and fit Isolation Forest model
        clf = IsolationForest(contamination=contamination_factor, random_state=42)
        clf.fit(X)

        # Predict outliers
        df["anomaly"] = clf.predict(X)
        df["anomaly"] = df["anomaly"].map(
            {1: 0, -1: 1}
        )  # Convert predictions to 0 (normal) or 1 (anomaly)

        output = {"model": clf, "columnX": columnX}

        return df, output

    return detect_anomalies


detect_anomalies = func()
