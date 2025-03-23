import csv
import datetime
from typing import Dict

from consumption import Consumption
from exception import ParserException


class OctopusParser:
    def __init__(self) -> None:
        self.buckets = {}
        self.half_hour_buckets_seen = []
        self.source = "octopus"

    def parse(self, file_path: str) -> Consumption:
        self.buckets = {}

        with open(file_path) as file:
            reader = csv.DictReader(file, skipinitialspace=True)
            for row in reader:
                self.process_row(row)

        self.validate_no_missing_buckets()

        return Consumption(self.source, self.buckets)

    def process_row(self, row: Dict[str, str]) -> None:
        start = datetime.datetime.fromisoformat(row["Start"]).replace(tzinfo=None)
        end = datetime.datetime.fromisoformat(row["End"]).replace(tzinfo=None)
        self.validate_times(start, end)

        bucket_start = start.replace(minute=0)

        if bucket_start not in self.buckets.keys():
            self.buckets[bucket_start] = 0

        self.buckets[bucket_start] += float(row["Consumption (kwh)"])
        self.half_hour_buckets_seen.append(start)

    def validate_times(self, start: datetime.datetime, end: datetime.datetime) -> None:
        pass
        if not self.is_exact_hour_or_half_hour(start):
            raise ParserException(f"start column of octopus csv is not an exact hour or half hour time, start={start}")

        if not self.is_exact_hour_or_half_hour(end):
            raise ParserException(f"end column of octopus csv is not an exact hour or half hour time, end={end}")

        if (end - start) != datetime.timedelta(minutes=30):
            raise ParserException(f"timespan of row from octopus csv is not exactly half an hour, start={start}, end={end}")

    @staticmethod
    def is_exact_hour_or_half_hour(the_datetime: datetime.datetime) -> bool:
        is_exact_hour = the_datetime.time() == datetime.time(hour=the_datetime.hour, minute=0)
        is_exact_half_hour = the_datetime.time() == datetime.time(hour=the_datetime.hour, minute=30)
        return is_exact_hour or is_exact_half_hour

    def validate_no_missing_buckets(self) -> None:
        first_bucket = min(self.half_hour_buckets_seen)
        last_bucket = max(self.half_hour_buckets_seen)

        checking_bucket = first_bucket
        while checking_bucket <= last_bucket:
            if checking_bucket not in self.half_hour_buckets_seen:
                raise ParserException(f"missing a half hourly bucket from the octopus csv, missing start={checking_bucket}")
            checking_bucket += datetime.timedelta(minutes=30)
