import csv
from datetime import datetime, timedelta, time
from typing import Dict, List

from data import Data
from exception import ParserException


class OctopusParser:
    def __init__(self, file_path: str, data: Data):
        self.file_path: str = file_path
        self.data: Data = data
        self.hourly_consumption: Dict[datetime, float] = {}
        self.half_hour_buckets_seen: List[datetime] = []

    def parse(self):
        with open(self.file_path) as file:
            reader = csv.DictReader(file, skipinitialspace=True)
            for row in reader:
                self.process_row(row)

        self.validate_no_missing_buckets()

        for hour, consumption in self.hourly_consumption.items():
            self.data.hourly.set_total_consumption(hour, consumption)

    def process_row(self, row: Dict[str, str]) -> None:
        start = datetime.fromisoformat(row["Start"]).replace(tzinfo=None)
        end = datetime.fromisoformat(row["End"]).replace(tzinfo=None)
        self.validate_times(start, end)

        hourly_bucket_start = start.replace(minute=0)

        if hourly_bucket_start not in self.hourly_consumption.keys():
            self.hourly_consumption[hourly_bucket_start] = 0

        self.hourly_consumption[hourly_bucket_start] += float(row["Consumption (kwh)"])
        self.half_hour_buckets_seen.append(start)

    def validate_times(self, start: datetime, end: datetime) -> None:
        pass
        if not self.is_exact_hour_or_half_hour(start):
            raise ParserException(f"start column of octopus csv is not an exact hour or half hour time, start={start}, file_path={self.file_path}")

        if not self.is_exact_hour_or_half_hour(end):
            raise ParserException(f"end column of octopus csv is not an exact hour or half hour time, end={end}, file_path={self.file_path}")

        if (end - start) != timedelta(minutes=30):
            raise ParserException(f"timespan of row from octopus csv is not exactly half an hour, start={start}, end={end}, file_path={self.file_path}")

    @staticmethod
    def is_exact_hour_or_half_hour(the_datetime: datetime) -> bool:
        is_exact_hour = the_datetime.time() == time(hour=the_datetime.hour, minute=0)
        is_exact_half_hour = the_datetime.time() == time(hour=the_datetime.hour, minute=30)
        return is_exact_hour or is_exact_half_hour

    def validate_no_missing_buckets(self) -> None:
        first_bucket = min(self.half_hour_buckets_seen)
        last_bucket = max(self.half_hour_buckets_seen)

        checking_bucket = first_bucket
        while checking_bucket <= last_bucket:
            if checking_bucket not in self.half_hour_buckets_seen:
                raise ParserException(
                    f"missing a half hourly bucket from the octopus csv, missing start={checking_bucket}, file_path={self.file_path}")
            checking_bucket += timedelta(minutes=30)
