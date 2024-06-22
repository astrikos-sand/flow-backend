def func(df, index):
    # Implement your logic here
    df.to_csv("csv_filename.csv", index=index)
    with open("csv_filename.csv", "rb") as file:
        content = file.read()
    return content


content = func(df, index)
