def func(c, db):
    # Implement your logic here
    data = {"key": 1001, "ts": 10001, "long_v": c}
    model = db.model("telemetry/insert")
    model.insert(data)
    return
