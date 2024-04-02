def fun(db, id):
    model = db.model("webhook-triggers")
    data = {"node": id}
    response = model.insert(data)
    return response


result = fun(db, id)
