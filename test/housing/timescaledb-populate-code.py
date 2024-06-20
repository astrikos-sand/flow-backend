def func(df, db):
    # Implement your logic here
    
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

    import json
    
    def chunkify(df, chunk_size):
        return [df[i : i + chunk_size] for i in range(0, df.shape[0], chunk_size)]

    chunks = chunkify(df, 100)
    
    columns = chunks[0].columns.to_list()
    
    for _, chunk in chunks[0].iterrows():
        for column in columns:
            data = {
                "ts": int(chunk["RowNumber"]),
                "key": COLUMNS[column],
            }
    
            if type(chunk[column]) == int:
                data["long_v"] = chunk[column]
            elif type(chunk[column]) == float:
                data["dbl_v"] = chunk[column]
            elif type(chunk[column]) == str:
                data["str_v"] = chunk[column]
            elif type(chunk[column]) == bool:
                data["bool_v"] = chunk[column]
            else:
                data["json_v"] = json.dumps(chunk[column])
    
            model = db.model("telemetry/insert")
            model.insert(data)
    return 

func(df, db)