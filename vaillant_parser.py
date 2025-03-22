import csv
import datetime
from typing import Dict

from Consumption import Consumption


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
            raise Exception(f"start column of vaillant csv is not an exact hour time, start={start}")

        if not self.is_exact_hour(end):
            raise Exception(f"end column of vaillant csv is not an exact hour time, end={end}")

        if (end - start) != datetime.timedelta(hours=1):
            raise Exception(f"timespan of row from vaillant csv is not exactly one hour, start={start}, end={end}")

    @staticmethod
    def is_exact_hour(the_datetime: datetime.datetime) -> bool:
        return the_datetime.time() == datetime.time(hour=the_datetime.hour, minute=0)
