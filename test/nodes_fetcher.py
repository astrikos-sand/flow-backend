def fun(db):
    model = db.model('nodes')
    response = model.get()
    return response

result = fun(db)