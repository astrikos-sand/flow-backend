def func(
    flow_df,
    config_details,
    mean_imputation,
    median_imputation,
    mode_imputation,
    bin_numerical_features,
    detect_anomalies,
    iterative_impute,
    impute_missing_values_with_rfc,
    delete_columns,
    delete_rows,
    row_deletion_using_colvalues,
    scale_numerical_variables,
    encode_categorical_variables,
    tree_based_feature_selection,
    pca_based_feature_selection,
    split_train_test_data,
    build_classification_models_rf,
    build_regression_models_rf,
    evaluate_classification_models,
    evaluate_regression_models,
    output_block,
    save_csv,
    download_file,
    new_df_url,
):
    # Implement your logic here
    import os
    import pandas as pd
    import pickle

    preprocessing_dict = {}

    print("***************************", flush=True)
    print("Save_csv", save_csv, flush=True)
    print("new_df_url", new_df_url, flush=True)
    print("flow_df", flow_df, flush=True)
    download_file("http://172.21.0.1:8000/media/uploads/Churndata.csv", "Churndata.csv")
    # check if the file is downloaded
    if os.path.exists("Churndata.csv"):
        print("File downloaded successfully", flush=True)
        # print the path of the downloaded file
        print("path to downloaded", os.path.abspath("Churndata.csv"), flush=True)
    else:
        print("File not downloaded", flush=True)

    print("***************************", flush=True)

    for index, row in flow_df.iterrows():
        print("-----------------------------------------", flush=True)
        print("function Name", row["FunctionName"], flush=True)

        if row["FunctionName"] == "config_details":
            print("***************************", flush=True)
            params = row["Input"]
            print("params", params, flush=True)
            print("input", row["Input"], flush=True)
            print("mode", row["Input"].get("mode"), flush=True)
            print("***************************", flush=True)
            preprocessing_dict_path = params.get("preprocessing_dict_path")
            file_exists = (
                os.path.exists(preprocessing_dict_path)
                if preprocessing_dict_path
                else False
            )
            Mode = "Predict"

            if row["Input"].get("mode") == Mode and file_exists:
                data, preprocessing_dict = config_details(params)
                output_block(preprocessing_dict, params.get("output_path"), data)
                break
            elif row["Input"].get("mode") == Mode and not file_exists:
                print("Your serialized pipeline is not found.")
                print("Before retraining the model, please ensure the following:")
                print("- Make sure all necessary variables are present in the dataset.")
                print(
                    "- Verify if the dataset used for training includes the target variable (Y)."
                )
                print(
                    "Once these steps are verified, you can proceed with retraining the model."
                )
                break
            else:
                config_details(params)
                print("config_details completed", flush=True)

        elif row["FunctionName"] in [
            "mean_imputation",
            "median_imputation",
            "mode_imputation",
            "bin_numerical_features",
            "detect_anomalies",
            "iterative_impute",
            "impute_missing_values_with_rfc",
            "delete_columns",
            "delete_rows",
            "row_deletion_using_colvalues",
            "scale_numerical_variables",
            "encode_categorical_variables",
            "tree_based_feature_selection",
            "pca_based_feature_selection",
        ]:
            df = None
            data_path = row["Input"][0]
            print("***************************", flush=True)
            print("data_path", data_path, flush=True)
            other_parameters = row["Input"][1] if len(row["Input"]) > 1 else None
            print("other_parameters", other_parameters, flush=True)

            if df is None:
                df = pd.read_csv(data_path)

            print("df", df, flush=True)

            input_params = [df] + ([other_parameters] if other_parameters else [])

            print("input_params", input_params, flush=True)
            print("***************************", flush=True)

            if row["FunctionName"] == "mean_imputation":
                df, values = mean_imputation(*input_params)
                preprocessing_dict["mean_imputation"] = values
            elif row["FunctionName"] == "median_imputation":
                df, values = median_imputation(*input_params)
                preprocessing_dict["median_imputation"] = values
            elif row["FunctionName"] == "mode_imputation":
                df, values = mode_imputation(*input_params)
                preprocessing_dict["mode_imputation"] = values
            elif row["FunctionName"] == "bin_numerical_features":
                df, bin_info = bin_numerical_features(*input_params)
                preprocessing_dict["bin_numerical_features"] = bin_info
            elif row["FunctionName"] == "detect_anomalies":
                df, anomaly_details = detect_anomalies(*input_params)
                preprocessing_dict["anomalies_info"] = anomaly_details
            elif row["FunctionName"] == "iterative_impute":
                df, columns = iterative_impute(*input_params)
                preprocessing_dict["iterative_imputation"] = columns
            elif row["FunctionName"] == "impute_missing_values_with_rfc":
                df, results = impute_missing_values_with_rfc(*input_params)
                preprocessing_dict["impute_missing_values_with_rfc"] = results
            elif row["FunctionName"] == "delete_columns":
                df = delete_columns(*input_params)
                preprocessing_dict["columns_to_delete"] = other_parameters
            elif row["FunctionName"] == "delete_rows":
                df = delete_rows(*input_params)
                preprocessing_dict["rows_to_delete"] = other_parameters
            elif row["FunctionName"] == "row_deletion_using_colvalues":
                df = row_deletion_using_colvalues(*input_params)
                preprocessing_dict["delete_rows_using_colvalues"] = other_parameters
            elif row["FunctionName"] == "scale_numerical_variables":
                df, scaled_output = scale_numerical_variables(*input_params)
                preprocessing_dict["normalized_features"] = scaled_output
            elif row["FunctionName"] == "encode_categorical_variables":
                df, label_encoders = encode_categorical_variables(*input_params)
                preprocessing_dict["label_encoders"] = label_encoders
            elif row["FunctionName"] == "tree_based_feature_selection":
                df, feature_selection_output = tree_based_feature_selection(
                    *input_params
                )
                preprocessing_dict["tree_based_feature_selection"] = (
                    feature_selection_output
                )
            elif row["FunctionName"] == "pca_based_feature_selection":
                df, pca_info = pca_based_feature_selection(*input_params)
                preprocessing_dict["pca_based_feature_selection"] = pca_info
            df.to_csv(data_path, index=False)
            save_csv(data_path)

        elif row["FunctionName"] == "split_train_test_data":
            df = None
            data_path = row["Input"][0]
            other_parameters = row["Input"][1:]

            if df is None:
                df = pd.read_csv(data_path)

            input_params = [df] + other_parameters
            X_train, X_test, y_train, y_test = split_train_test_data(*input_params)

            X_train.to_csv("X_train.csv", index=False)
            save_csv("X_train.csv")
            X_test.to_csv("X_test.csv", index=False)
            save_csv("X_test.csv")
            y_train.to_csv("y_train.csv", index=False)
            save_csv("y_train.csv")
            y_test.to_csv("y_test.csv", index=False)
            save_csv("y_test.csv")

        elif row["FunctionName"] in [
            "build_classification_models_rf",
            "build_regression_models_rf",
        ]:
            print("***************************", flush=True)
            print("row input", row["Input"], flush=True)
            X_train = X_test = y_train = y_test = None
            X_train_data_path, X_test_data_path, y_train_data_path, y_test_data_path = (
                row["Input"][:4]
            )
            other_parameters = row["Input"][4:]

            print("X_train_data_path", X_train_data_path, flush=True)
            print("X_test_data_path", X_test_data_path, flush=True)
            print("y_train_data_path", y_train_data_path, flush=True)
            print("y_test_data_path", y_test_data_path, flush=True)
            print("other_parameters", other_parameters, flush=True)

            # check if path exists
            if os.path.exists(X_train_data_path):
                print("X_train_data_path exists", flush=True)
            if os.path.exists(X_test_data_path):
                print("X_test_data_path exists", flush=True)
            if os.path.exists(y_train_data_path):
                print("y_train_data_path exists", flush=True)
            if os.path.exists(y_test_data_path):
                print("y_test_data_path exists", flush=True)
        
            if X_train is None:
                X_train = pd.read_csv(X_train_data_path)
            if X_test is None:
                X_test = pd.read_csv(X_test_data_path)
            if y_train is None:
                y_train = pd.read_csv(y_train_data_path)
                print("y_train", y_train, flush=True)
                print("y_train columns", y_train.columns, flush=True)
                y_train = y_train[y_train.columns[0]]
            if y_test is None:
                y_test = pd.read_csv(y_test_data_path)
                y_test = y_test[y_test.columns[0]]

            input_params = [X_train, y_train, X_test, y_test] + other_parameters

            print("input_params", input_params, flush=True)
            print("***************************", flush=True)

            if row["FunctionName"] == "build_classification_models_rf":
                model, X_test, y_test = build_classification_models_rf(*input_params)
            else:
                model, X_test, y_test = build_regression_models_rf(*input_params)

            with open("trained_models.pkl", "wb") as file:
                pickle.dump(model, file)
                save_csv("trained_models.pkl")
            X_test.to_csv("X_test.csv", index=False)
            save_csv("X_test.csv")
            y_test.to_csv("y_test.csv", index=False)
            save_csv("y_test.csv")

        elif row["FunctionName"] in [
            "evaluate_classification_models",
            "evaluate_regression_models",
        ]:
            trained_model_path = row["Input"][0]
            with open(trained_model_path, "rb") as file:
                loaded_models = pickle.load(file)
                save_csv(trained_model_path)

            X_test = y_test = None
            if X_test is None:
                X_test = pd.read_csv(X_test_data_path)
            if y_test is None:
                y_test = pd.read_csv(y_test_data_path)
                y_test = y_test[y_test.columns[0]]

            other_parameters = row["Input"][3:]
            input_params = [loaded_models, X_test, y_test] + other_parameters
            if row["FunctionName"] == "evaluate_classification_models":
                best_model, evaluation_metrics = evaluate_classification_models(
                    *input_params
                )
            else:
                best_model, evaluation_metrics = evaluate_regression_models(
                    *input_params
                )

            preprocessing_dict["best_model"] = best_model
            with open("best_model.pkl", "wb") as file:
                pickle.dump(best_model, file)

            if os.path.exists("best_model.pkl"):
                print("best_model.pkl exists", flush=True)
                save_csv("best_model.pkl")
            else:
                print("best_model.pkl does not exist", flush=True)

            with open("evaluation_metrics.pkl", "wb") as file:
                pickle.dump(evaluation_metrics, file)
            
            if os.path.exists("evaluation_metrics.pkl"):
                print("evaluation_metrics.pkl exists", flush=True)
                save_csv("evaluation_metrics.pkl")
            else:
                print("evaluation_metrics.pkl does not exist", flush=True)

        elif row["FunctionName"] == "output_block":
            path = row["Input"][0]
            input_params = [preprocessing_dict, path]
            output_block(*input_params)
    ok = "ok"
    return ok


ok = func(
    flow_df,
    config_details,
    mean_imputation,
    median_imputation,
    mode_imputation,
    bin_numerical_features,
    detect_anomalies,
    iterative_impute,
    impute_missing_values_with_rfc,
    delete_columns,
    delete_rows,
    row_deletion_using_colvalues,
    scale_numerical_variables,
    encode_categorical_variables,
    tree_based_feature_selection,
    pca_based_feature_selection,
    split_train_test_data,
    build_classification_models_rf,
    build_regression_models_rf,
    evaluate_classification_models,
    evaluate_regression_models,
    output_block,
    save_csv,
    download_file,
    new_df_url,
)
