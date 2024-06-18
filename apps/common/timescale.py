from django.db import connections


def execute_timescale_query(query):
    with connections["timescaledb"].cursor() as cursor:
        cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()
