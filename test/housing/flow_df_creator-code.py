def func(df, save_csv):
    # Implement your logic here
    import pandas as pd

    new_df = df.drop(["Exited"], axis=1)
    new_df.to_csv("new_df.csv")
    save_csv("new_df.csv")

    # Mode Predict
    # data = {
    #     "FunctionName": [
    #         "config_details",
    #         "encode_categorical_variables",
    #         "split_train_test_data",
    #         "build_classification_models_rf",
    #         "evaluate_classification_models",
    #         "output_block",
    #     ],
    #     "Input": [
    #         {
    #             "csv_path": "new_df.csv",
    #             "mode": "Predict",
    #             "preprocessing_dict_path": "output_json.pkl",
    #             "output_path": "predicted.csv",
    #         },
    #         ["copied_data.csv", ["Geography", "Gender"]],
    #         [
    #             "copied_data.csv",
    #             "Exited",
    #             [
    #                 "CreditScore",
    #                 "Age",
    #                 "Tenure",
    #                 "Balance",
    #                 "EstimatedSalary",
    #                 "Geography_encoded",
    #                 "Gender_encoded",
    #             ],
    #         ],
    #         [
    #             "X_train.csv",
    #             "X_test.csv",
    #             "y_train.csv",
    #             "y_test.csv",
    #             None,
    #             [
    #                 {
    #                     "n_estimators": 200,
    #                     "max_depth": 10,
    #                     "min_samples_split": 5,
    #                     "min_samples_leaf": 2,
    #                     "max_features": "log2",
    #                     "bootstrap": True,
    #                 },
    #                 {
    #                     "n_estimators": 300,
    #                     "max_depth": 20,
    #                     "min_samples_split": 10,
    #                     "min_samples_leaf": 4,
    #                     "max_features": "sqrt",
    #                     "bootstrap": True,
    #                 },
    #                 {
    #                     "n_estimators": 400,
    #                     "max_depth": 30,
    #                     "min_samples_split": 15,
    #                     "min_samples_leaf": 6,
    #                     "max_features": 0.5,
    #                     "bootstrap": False,
    #                 },
    #             ],
    #         ],
    #         ["trained_models.pkl", "X_test.csv", "y_test.csv"],
    #         ["output_json.pkl"],
    #     ],
    # }


    # Mode Train
    data = {
        "FunctionName": [
            "config_details",
            "encode_categorical_variables",
            "split_train_test_data",
            "build_classification_models_rf",
            "evaluate_classification_models",
            "output_block",
        ],
        "Input": [
            {"csv_path": "Churndata.csv", "mode": "Train"},
            ["copied_data.csv", ["Geography", "Gender"]],
            [
                "copied_data.csv",
                "Exited",
                [
                    "CreditScore",
                    "Age",
                    "Tenure",
                    "Balance",
                    "EstimatedSalary",
                    "Geography_encoded",
                    "Gender_encoded",
                ],
            ],
            [
                "X_train.csv",
                "X_test.csv",
                "y_train.csv",
                "y_test.csv",
                None,
                [
                    {
                        "n_estimators": 200,
                        "max_depth": 10,
                        "min_samples_split": 5,
                        "min_samples_leaf": 2,
                        "max_features": "log2",
                        "bootstrap": True,
                    },
                    {
                        "n_estimators": 300,
                        "max_depth": 20,
                        "min_samples_split": 10,
                        "min_samples_leaf": 4,
                        "max_features": "sqrt",
                        "bootstrap": True,
                    },
                    {
                        "n_estimators": 400,
                        "max_depth": 30,
                        "min_samples_split": 15,
                        "min_samples_leaf": 6,
                        "max_features": 0.5,
                        "bootstrap": False,
                    },
                ],
            ],
            ["trained_models.pkl", "X_test.csv", "y_test.csv"],
            ["output_json.pkl"],
        ],
    }

    # Create the DataFrame
    flow_df = pd.DataFrame(data)
    return flow_df


flow_df = func(df, save_csv)
