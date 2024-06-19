def fun(db):
    model = db.model("telemetry/query")
    data = {
        "start": "1718013400000",
        "end": "1718013500000",
        "key": 21,
    }
    response = model.insert(data)
    return response


response = fun(db)
