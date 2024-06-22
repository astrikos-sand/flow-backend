def func(db):
    # Implement your logic here
    model = db.model("telemetry/query")
    data = {
        "start": "1718013400000",
        "end": "1718013500000",
        "key": 21,
    }
    c = model.insert(data)
    return c


c = func(db)
