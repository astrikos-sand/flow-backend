def func(db, dbname, user, password, host, port):
    # Implement your logic here
    connector = db.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port,
    )
    connector.cursor.execute("SELECT * FROM flow_flowfile;")
    res = connector.cursor.fetchall()
    connector.close()
    print(res, flush=True)

    return res


res = func(db, dbname, user, password, host, port)
