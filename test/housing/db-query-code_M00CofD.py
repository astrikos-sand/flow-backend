def func(c, db):
    # Implement your logic here
    data = {"ts": 1000, "key": 1200, "long_v": c}
    model = db.model("telemetry/insert")
    model.insert(data)
    return
