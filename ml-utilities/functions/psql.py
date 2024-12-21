def func(server, database, username=None, password=None, port=5432):
    """
    Establishes a connection to a PostgreSQL database and returns the connection object.

    Parameters:
        server (str): The server name or IP address.
        database (str): The name of the database to connect to.
        username (str, optional): The username for PostgreSQL authentication.
        password (str, optional): The password for PostgreSQL authentication.
        port (int, optional): The port number. Default is 5432.

    Returns:
        psycopg2.extensions.connection: The connection object.
    """
    import psycopg2

    try:
        connection = psycopg2.connect(
            host=server, database=database, user=username, password=password, port=port
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error while connecting to PostgreSQL: {e}")
        raise


connection = func(server, database, username, password, port)
