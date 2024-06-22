def func(content):
    # Implement your logic here
    with open("csv_path.csv", "wb") as f:
        f.write(content)
    import pandas as pd

    print("Starting training/retraining...")
    original_df = pd.read_csv("csv_path.csv")
    return original_df


original_df = func(content)
