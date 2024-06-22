def func(db):
    # Implement your logic here
    connector = db.connect(
        dbname="astrikos_db",
        user="dummy",
        password="dummy",
        host="localhost",
        port="5436",
    )
    connector.cursor.execute("SELECT * FROM flow_slot;")
    res = connector.cursor.fetchall()
    connector.close()
    print(type(res), flush=True)

    return res


res = func(db)
