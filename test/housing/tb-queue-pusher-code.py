def func(res, tbq):
    # Implement your logic here
    producer = tbq.producer()
    import json

    data = {
        "temperture": 30,
    }
    producer.publish(json.dumps(data), "tb_core.9")
    return


func(res, tbq)
