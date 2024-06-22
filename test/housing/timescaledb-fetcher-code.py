def func(db):
    import pandas as pd

    # Implement your logic here
    model = db.model("telemetry/query")
    data = {
        "start": 0,
        "end": 101,
    }
    response = model.insert(data)
    COLUMNS = {
        "RowNumber": 100,
        "CustomerId": 101,
        "Surname": 102,
        "CreditScore": 103,
        "Geography": 104,
        "Gender": 105,
        "Age": 106,
        "Tenure": 107,
        "Balance": 108,
        "NumOfProducts": 109,
        "HasCrCard": 110,
        "IsActiveMember": 111,
        "EstimatedSalary": 112,
        "Exited": 113,
    }

    def get_column_name(key):
        for column, value in COLUMNS.items():
            if value == key:
                return column
        return None

    data = [{} for _ in range(102)]
    for res in response:
        data[res[2] - 1] = {
            **data[res[2] - 1],
            get_column_name(res[1]): res[5] or res[4] or res[6] or res[3] or res[7],
        }

    df = pd.DataFrame(data)
    print(df, flush=True)
    return df


df = func(db)
