def fun(db):
    model = db.model("resources")
    data = {"name": "mdg123", "resource_type": "test", "data": {
        "kpis": [
            {
                "kpi": "kpi1",
                "value": 10,
                "time": "2020-01-01T00:00:00Z",
            }
        ]
    }}
    response = model.insert(data)
    return response


result = fun(db)
