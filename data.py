from datetime import datetime
from typing import Dict

from dateutil.relativedelta import relativedelta

from tariff import Tariff


class Consumption:
    def __init__(self):
        self.dhw: float | None = None
        self.heating: float | None = None
        self.heat_pump: float | None = None
        self.non_heat_pump: float | None = None
        self.total: float | None = None

    def set_to_zero(self):
        self.dhw = 0
        self.heating = 0
        self.heat_pump = 0
        self.non_heat_pump = 0
        self.total = 0


class TariffPrices:
    def __init__(self, tariff: Tariff):
        self.tariff: Tariff = tariff
        self.dhw: float | None = None
        self.heating: float | None = None
        self.heat_pump: float | None = None
        self.non_heat_pump: float | None = None
        self.standing_charge: float | None = None
        self.total: float | None = None

    def set_to_zero(self):
        self.dhw = 0
        self.heating = 0
        self.heat_pump = 0
        self.non_heat_pump = 0
        self.standing_charge = 0
        self.total = 0


class BucketData:
    def __init__(self, start: datetime, end: datetime):
        self.start: datetime = start
        self.end: datetime = end
        self.consumption_kwh: Consumption = Consumption()
        self.tariff_prices_pence: Dict[str, TariffPrices] = {}


class TimeBucketedData:
    def __init__(self, timespan: relativedelta):
        self.buckets: Dict[datetime, BucketData] = {}
        self.timespan: relativedelta = timespan

    def at_start(self, start: datetime) -> BucketData:
        return self.buckets[start]

    def set_heat_pump_consumption(self, start: datetime, dhw: float, heating: float):
        self.ensure_bucket_exists(start)
        self.at_start(start).consumption_kwh.dhw = dhw
        self.at_start(start).consumption_kwh.heating = heating
        self.at_start(start).consumption_kwh.heat_pump = dhw + heating
        self.calculate_non_heat_pump_consumption(start)

    def set_total_consumption(self, start, consumption):
        self.ensure_bucket_exists(start)
        self.at_start(start).consumption_kwh.total = consumption
        self.calculate_non_heat_pump_consumption(start)

    def calculate_non_heat_pump_consumption(self, start):
        consumption = self.at_start(start).consumption_kwh
        if consumption.total is not None and consumption.heat_pump is not None:
            consumption.non_heat_pump = consumption.total - consumption.heat_pump

    def ensure_bucket_exists(self, start):
        if start not in self.buckets.keys():
            self.buckets[start] = BucketData(start, start + self.timespan)

    def first_bucket_start(self):
        min_key = min(self.buckets.keys())
        return self.buckets[min_key].start

    def last_bucket_end(self):
        max_key = max(self.buckets.keys())
        return self.buckets[max_key].end


class Data:
    def __init__(self):
        self.hourly: TimeBucketedData = TimeBucketedData(relativedelta(hours=1))
        self.daily: TimeBucketedData = TimeBucketedData(relativedelta(days=1))
        self.monthly: TimeBucketedData = TimeBucketedData(relativedelta(months=1))
        self.yearly: TimeBucketedData = TimeBucketedData(relativedelta(years=1))
        self.total: BucketData | None = None
