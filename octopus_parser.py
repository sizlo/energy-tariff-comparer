import csv
import datetime
from typing import Dict

from Consumption import Consumption


class OctopusParser:
    def __init__(self) -> None:
        self.buckets = {}
        self.source = "octopus"

    def parse(self, file_path: str) -> Consumption:
        self.buckets = {}

        with open(file_path) as file:
            reader = csv.DictReader(file, skipinitialspace=True)
            for row in reader:
                self.process_row(row)

        return Consumption(self.source, self.buckets)

    def process_row(self, row: Dict[str, str]) -> None:
        start = datetime.datetime.fromisoformat(row["Start"]).replace(tzinfo=None)
        end = datetime.datetime.fromisoformat(row["End"]).replace(tzinfo=None)
        self.validate_times(start, end)

        bucket_start = start.replace(minute=0)

        if bucket_start not in self.buckets.keys():
            self.buckets[bucket_start] = 0

        self.buckets[bucket_start] += float(row["Consumption (kwh)"])

    def validate_times(self, start: datetime.datetime, end: datetime.datetime) -> None:
        pass
        if not self.is_exact_hour_or_half_hour(start):
            raise Exception(f"start column of octopus csv is not an exact hour or half hour time, start={start}")

        if not self.is_exact_hour_or_half_hour(end):
            raise Exception(f"end column of octopus csv is not an exact hour or half hour time, end={end}")

        if (end - start) != datetime.timedelta(minutes=30):
            raise Exception(f"timespan of row from octopus csv is not exactly half an hour, start={start}, end={end}")

    @staticmethod
    def is_exact_hour_or_half_hour(the_datetime: datetime.datetime) -> bool:
        is_exact_hour = the_datetime.time() == datetime.time(hour=the_datetime.hour, minute=0)
        is_exact_half_hour = the_datetime.time() == datetime.time(hour=the_datetime.hour, minute=30)
        return is_exact_hour or is_exact_half_hour
