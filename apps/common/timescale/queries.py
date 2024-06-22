class QUERIES:
    START_END_KEY = """
            SELECT *
            FROM ts_kv
            WHERE ts >= {start}
            AND ts <= {end};
        """
