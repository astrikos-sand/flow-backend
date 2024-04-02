import influxdb_client
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

import config.const as const


class InfluxDB:
    def __init__(self) -> None:
        self.client = self.connect()

    def connect(self) -> InfluxDBClient:
        return influxdb_client.InfluxDBClient(
            url=const.INFLUXDB_URI, token=const.INFLUXDB_TOKEN, org=const.INFLUXDB_ORG
        )

    def write(self, data: dict) -> None:
        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        if data.get("kpi"):
            record = (
                influxdb_client.Point(data["measurement"])
                .field(data["kpi"], data["value"])
                .time(data["time"])
            )
            write_api.write(
                bucket=const.INFLUXDB_BUCKET, org=const.INFLUXDB_ORG, record=record
            )
        if data.get("non_timeseries_data"):
            fixed_timestamp = datetime(
                year=2024, month=4, day=1, hour=0, minute=0, second=0
            )
            print(data["non_timeseries_data"])
            for entry in data["non_timeseries_data"]:
                for key, value in entry.items():
                    print(key, value)
                    record = (
                        influxdb_client.Point(data["measurement"])
                        .field(key, value)
                        .time(fixed_timestamp)
                    )
                    write_api.write(
                        bucket=const.INFLUXDB_BUCKET, org=const.INFLUXDB_ORG, record=record
                    )
        write_api.__del__()

    def get_data(self, query: str) -> list:
        query_api = self.client.query_api()
        res = query_api.query(org=const.INFLUXDB_ORG, query=query)
        query_api.__del__()

        result = []
        for table in res:
            for record in table.records:
                result.append(record.values)

        return result
