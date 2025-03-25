import csv
import datetime
from typing import Dict, List

from data import Data
from exception import ParserException


class VaillantParser:
    def __init__(self, file_path: str, data: Data):
        self.file_path: str = file_path
        self.data: Data = data
        self.processed_buckets: List[datetime] = []

    def parse(self):
        with open(self.file_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.process_row(row)

        self.validate_no_missing_buckets()

    def process_row(self, row: Dict[str, str]) -> None:
        start = datetime.datetime.strptime(row["start"], "%Y-%m-%dT%H:%M")
        end = datetime.datetime.strptime(row["end"], "%Y-%m-%dT%H:%M")
        self.validate_times(start, end)

        dhw_usage = float(row["DOMESTIC_HOT_WATER.CONSUMED_ELECTRICAL_ENERGY"]) / 1000.0
        heating_usage = float(row["HEATING.CONSUMED_ELECTRICAL_ENERGY"]) / 1000.0

        self.data.hourly.set_heat_pump_consumption(start, dhw_usage, heating_usage)

        self.processed_buckets.append(start)

    def validate_times(self, start: datetime.datetime, end: datetime.datetime) -> None:
        if not self.is_exact_hour(start):
            raise ParserException(f"start column of vaillant csv is not an exact hour time, start={start}, file_path={self.file_path}")

        if not self.is_exact_hour(end):
            raise ParserException(f"end column of vaillant csv is not an exact hour time, end={end}, file_path={self.file_path}")

        if (end - start) != datetime.timedelta(hours=1):
            raise ParserException(f"timespan of row from vaillant csv is not exactly one hour, start={start}, end={end}, file_path={self.file_path}")

    @staticmethod
    def is_exact_hour(the_datetime: datetime.datetime) -> bool:
        return the_datetime.time() == datetime.time(hour=the_datetime.hour, minute=0)

    def validate_no_missing_buckets(self) -> None:
        first_bucket = min(self.processed_buckets)
        last_bucket = max(self.processed_buckets)

        checking_bucket = first_bucket
        while checking_bucket <= last_bucket:
            if checking_bucket not in self.processed_buckets:
                raise ParserException(f"missing an hourly bucket from the vaillant csv, missing start={checking_bucket}, file_path={self.file_path}")
            checking_bucket += datetime.timedelta(hours=1)
