from datetime import timedelta

from data import Data, BucketData, TariffPrices


class BucketRollUpper:
    def __init__(self, data: Data):
        self.data = data

    def roll_up(self):
        self.roll_up_days()
        self.roll_up_months()
        self.roll_up_years()
        self.roll_up_total()

    def roll_up_days(self):
        for hour_bucket in self.data.hourly.buckets.values():
            day_start = hour_bucket.start.replace(hour=0)
            self.data.daily.ensure_bucket_exists(day_start)
            day_bucket = self.data.daily.at_start(day_start)
            self.add_consumption_and_prices_to_bucket(hour_bucket, day_bucket)

        for day_bucket in self.data.daily.buckets.values():
            for tariff_prices in day_bucket.tariff_prices_pence.values():
                tariff_prices.standing_charge = tariff_prices.tariff.daily_standing_charge_pence
                tariff_prices.total += tariff_prices.standing_charge

    def roll_up_months(self):
        for day_bucket in self.data.daily.buckets.values():
            month_start = day_bucket.start.replace(day=1)
            self.data.monthly.ensure_bucket_exists(month_start)
            month_bucket = self.data.monthly.at_start(month_start)
            self.add_consumption_and_prices_to_bucket(day_bucket, month_bucket)

    def roll_up_years(self):
        for month_bucket in self.data.monthly.buckets.values():
            year_start = month_bucket.start.replace(month=1)
            self.data.yearly.ensure_bucket_exists(year_start)
            year_bucket = self.data.yearly.at_start(year_start)
            self.add_consumption_and_prices_to_bucket(month_bucket, year_bucket)

    def roll_up_total(self):
        self.data.total = BucketData(self.data.hourly.first_bucket_start(), self.data.hourly.last_bucket_end())
        self.data.total.consumption_kwh.set_to_zero()
        for year_bucket in self.data.yearly.buckets.values():
            self.add_consumption_and_prices_to_bucket(year_bucket, self.data.total)

    @staticmethod
    def add_consumption_and_prices_to_bucket(from_bucket: BucketData, to_bucket: BucketData):
        if to_bucket.consumption_kwh.total is None:
            to_bucket.consumption_kwh.set_to_zero()

        to_bucket.consumption_kwh.dhw += from_bucket.consumption_kwh.dhw
        to_bucket.consumption_kwh.heating += from_bucket.consumption_kwh.heating
        to_bucket.consumption_kwh.heat_pump += from_bucket.consumption_kwh.heat_pump
        to_bucket.consumption_kwh.non_heat_pump += from_bucket.consumption_kwh.non_heat_pump
        to_bucket.consumption_kwh.total += from_bucket.consumption_kwh.total

        for from_tariff_prices in from_bucket.tariff_prices_pence.values():
            name = from_tariff_prices.tariff.name

            if name not in to_bucket.tariff_prices_pence.keys():
                new_tariff_prices = TariffPrices(from_tariff_prices.tariff)
                new_tariff_prices.set_to_zero()
                to_bucket.tariff_prices_pence[name] = new_tariff_prices

            to_tariff_prices = to_bucket.tariff_prices_pence[name]

            to_tariff_prices.dhw += from_tariff_prices.dhw
            to_tariff_prices.heating += from_tariff_prices.heating
            to_tariff_prices.heat_pump += from_tariff_prices.heat_pump
            to_tariff_prices.non_heat_pump += from_tariff_prices.non_heat_pump
            to_tariff_prices.total += from_tariff_prices.total

            if from_tariff_prices.standing_charge is not None:
                to_tariff_prices.standing_charge += from_tariff_prices.standing_charge
