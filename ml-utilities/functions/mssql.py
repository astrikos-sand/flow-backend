def func(server, database, username, password, driver, port):
    """
    Establishes a connection to an MSSQL database and returns the connection object.

    Parameters:
        server (str): The server name or IP address.
        database (str): The name of the database to connect to.
        username (str, optional): The username for SQL Server Authentication.
        password (str, optional): The password for SQL Server Authentication.
        trusted_connection (bool): Use Windows Authentication if True. Default is True.
        driver (str): ODBC driver name. Default is "ODBC Driver 17 for SQL Server".
        port (int, optional): The port number if not using the default port 1433.

    Returns:
        pyodbc.Connection: The connection object.
    """
    import pyodbc

    conn_str = (
        f"Driver={{{driver}}};"
        f"Server={server}{',' + str(port) if port else ''};"
        f"Database={database};"
        f"UID={username};"
        f"PWD={password};"
    )

    connection = pyodbc.connect(conn_str)
    return connection


connection = func(server, database, username, password, driver, port)
