def func(connection, start, end, entity_id):
    """
    Fetch records from ts_kv table within the specified time range and entity ID.

    :param start: Start timestamp in milliseconds.
    :param end: End timestamp in milliseconds.
    :param entity_id: Entity ID as a string.
    :return: List of records matching the criteria.
    """
    try:
        # Create a cursor object
        cursor = connection.cursor()

        # Define the SQL query
        query = """
            SELECT *
            FROM ts_kv
            WHERE ts BETWEEN %s AND %s
              AND entity_id = %s
            ORDER BY ts DESC;
        """

        # Execute the query
        cursor.execute(query, (start, end, entity_id))

        # Fetch all results
        records = cursor.fetchall()
        cursor.close()

        return records

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return []


records = func(connection, start, end, entity_id)
