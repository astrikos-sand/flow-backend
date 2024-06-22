def func():
    # Implement your logic here
    def delete_columns(df, columns):
        import pandas as pd

        if isinstance(columns, str):
            columns = [columns]

        # Drop specified columns
        df.drop(columns=columns, inplace=True)

        return df

    return delete_columns


delete_columns = func()
