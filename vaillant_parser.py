import csv
import datetime
from typing import Dict

from consumption import Consumption
from exception import ParserException


class VaillantParser:
    def __init__(self) -> None:
        self.buckets = {}
        self.source = "vaillant"

    def parse(self, file_path: str) -> Consumption:
        self.buckets = {}

        with open(file_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.process_row(row)

        self.validate_no_missing_buckets()

        return Consumption(self.source, self.buckets)

    def process_row(self, row: Dict[str, str]) -> None:
        start = datetime.datetime.strptime(row["start"], "%Y-%m-%dT%H:%M")
        end = datetime.datetime.strptime(row["end"], "%Y-%m-%dT%H:%M")
        self.validate_times(start, end)

        dhw_usage = float(row["DOMESTIC_HOT_WATER.CONSUMED_ELECTRICAL_ENERGY"])
        heating_usage = float(row["HEATING.CONSUMED_ELECTRICAL_ENERGY"])

        self.buckets[start] = (dhw_usage + heating_usage) / 1000.0

    def validate_times(self, start: datetime.datetime, end: datetime.datetime) -> None:
        if not self.is_exact_hour(start):
            raise ParserException(f"start column of vaillant csv is not an exact hour time, start={start}")

        if not self.is_exact_hour(end):
            raise ParserException(f"end column of vaillant csv is not an exact hour time, end={end}")

        if (end - start) != datetime.timedelta(hours=1):
            raise ParserException(f"timespan of row from vaillant csv is not exactly one hour, start={start}, end={end}")

    @staticmethod
    def is_exact_hour(the_datetime: datetime.datetime) -> bool:
        return the_datetime.time() == datetime.time(hour=the_datetime.hour, minute=0)

    def validate_no_missing_buckets(self) -> None:
        first_bucket = min(self.buckets.keys())
        last_bucket = max(self.buckets.keys())

        checking_bucket = first_bucket
        while checking_bucket <= last_bucket:
            if checking_bucket not in self.buckets.keys():
                raise ParserException(f"missing an hourly bucket from the vaillant csv, missing start={checking_bucket}")
            checking_bucket += datetime.timedelta(hours=1)
