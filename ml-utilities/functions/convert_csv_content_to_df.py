def func(csv_content):
    import pandas as pd
    import io

    df = pd.read_csv(io.StringIO(csv_content.decode("utf-8")))
    return df


df = func(csv_content)
