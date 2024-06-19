class QUERIES:
    START_END_KEY = """
            SELECT *
            FROM ts_kv
            WHERE key = {key}
            AND ts >= {start}
            AND ts <= {end};
        """
