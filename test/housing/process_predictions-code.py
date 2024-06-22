def func(flow_df, config_details, output_block, download_file, trained_model_url):
    # Implement your logic here
    import os

    for _, row in flow_df.iterrows():
        if row["FunctionName"] == "config_details":
            params = row["Input"]

            preprocessing_dict_path = params.get("preprocessing_dict_path")
            print("preprocessing_dict_path", preprocessing_dict_path, flush=True)
            print("trained_model_url", trained_model_url, flush=True)
            download_file(trained_model_url, preprocessing_dict_path)
            download_file(
                "http://172.21.0.1:8000/media/uploads/new_df.csv", "new_df.csv"
            )

            if preprocessing_dict_path is not None:
                file_exists = os.path.exists(preprocessing_dict_path)
            else:
                file_exists = False

            print("File exists status", file_exists, flush=True)

            # define the mode
            Mode = "Predict"

            if row["Input"].get("mode") == Mode and file_exists:
                data, preprocessing_dict = config_details(params)
                # prediction
                output_block(preprocessing_dict, params.get("output_path"), data)

            break

    ok = "ok"
    return ok


ok = func(flow_df, config_details, output_block, download_file, trained_model_url)
