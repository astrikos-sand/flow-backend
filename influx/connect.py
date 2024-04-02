from datetime import datetime
import pytz

import influxdb_client
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

import config.const as const


class InfluxDB:
    def __init__(self) -> None:
        self.client = self.connect()
        self.fixed_timestamp_start = datetime(
            year=2000, month=4, day=1, hour=0, minute=0, second=0, tzinfo=pytz.UTC
        ).isoformat()
        self.fixed_timestamp_stop = datetime(
            year=2000, month=4, day=2, hour=0, minute=0, second=0, tzinfo=pytz.UTC
        ).isoformat()

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

            try:
                write_api.write(
                    bucket=const.INFLUXDB_BUCKET, org=const.INFLUXDB_ORG, record=record
                )
            except Exception as e:
                print(e, flush=True)

        if data.get("non_timeseries_data"):
            for key, value in data["non_timeseries_data"].items():
                record = (
                    influxdb_client.Point(data["measurement"])
                    .field(key, value)
                    .time(self.fixed_timestamp_start)
                )
                try:
                    write_api.write(
                        bucket=const.INFLUXDB_BUCKET,
                        org=const.INFLUXDB_ORG,
                        record=record,
                    )
                except Exception as e:
                    print(e, flush=True)

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
