def func(content):
    # Implement your logic here
    with open("csv_path.csv", "wb") as f:
        f.write(content)
    import pandas as pd

    print("Starting training/retraining...")
    df = pd.read_csv("csv_path.csv")
    return df


df = func(content)
