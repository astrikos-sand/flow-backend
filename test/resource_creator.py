def fun(db):
    model = db.model("resources")
    data = {
        "name": "mdg123",
        "resource_type": "test",
        "data": {
            "kpis": [
                {
                    "kpi": "kpi1",
                    "value": 10,
                    "time": "2020-01-01T00:00:00Z",
                }
            ],
            "start_time": "-4000d",
            "server_id": "server1233",
            "server_name": "server1233",
            "server_type": "server1233",
        },
    }
    response = model.insert(data)
    return response


response = fun(db)
