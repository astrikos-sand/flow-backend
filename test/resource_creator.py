def fun(db):
    model = db.model('resources')
    data = {
        'name': 'testing',
        'resource_type': 'test',
        'data': {
            'key': 'value'
        }
    }
    response = model.insert(data)
    return response

result = fun(db)