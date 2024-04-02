def fun(db):
    model = db.model("nodes")
    response = model.get()
    return response


response = fun(db)
