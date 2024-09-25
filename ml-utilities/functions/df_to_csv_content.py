def func(df):
    import io

    with io.BytesIO() as f:
        df.to_csv(f, index=False)
        f.seek(0)
        csv_content = f.getvalue()

    return csv_content


csv_content = func(df)
