def func(count, df):
    # Implement your logic here
    print(count, flush=True)
    df_heads = df.head(count)
    print(df_heads, flush=True)
    return df_heads


df_heads = func(count, df)
