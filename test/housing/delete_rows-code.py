def func():
    # Implement your logic here
    def delete_rows(df, rows_to_delete, exclude_include="exclude"):
        import pandas as pd

        df_length = len(df)
        parsed_indices = []
        for index in rows_to_delete:
            if isinstance(index, str) and ":" in index:
                start, end = map(
                    lambda x: int(x) if x != "" else None, index.split(":")
                )
                if start is None:
                    start = 0
                if end is None:
                    end = df_length
                parsed_indices.extend(list(range(start, end)))
            else:
                parsed_indices.append(int(index))

        if exclude_include == "exclude":
            # Exclude specified rows
            excluded_rows = df.iloc[~df.index.isin(parsed_indices)]
            return excluded_rows
        elif exclude_include == "include":
            # Include only specified rows
            included_rows = df.iloc[df.index.isin(parsed_indices)]
            return included_rows
        else:
            raise ValueError(
                "Invalid value for 'exclude_include'. Must be 'exclude' or 'include'."
            )

    return delete_rows


delete_rows = func()
