from typing import List

from bucket_roll_upper import BucketRollUpper
from data import Data
from hourly_price_calculator import HourlyPriceCalculator
from exception import MismatchedBucketsException
from tariff import Tariff
from util import render_price


class Comparer:
    def __init__(self, data: Data, tariffs: List[Tariff]):
        self.data = data
        self.tariffs = tariffs

        self.validate_both_consumptions_have_same_buckets()
        self.increase_total_consumption_when_heat_pump_consumption_is_greater_than_total_consumption()

    def compare(self, output_csvs: bool = False):
        for tariff in self.tariffs:
            HourlyPriceCalculator(self.data, tariff).calculate()
        BucketRollUpper(self.data).roll_up()

        sorted_total_prices = sorted(self.data.total.tariff_prices_pence.values(), key=lambda prices: prices.total)

        print("**** Total price for entire period of input data for each tariff ****")
        for total_prices in sorted_total_prices:
            print(f"{total_prices.tariff.name}: {render_price(total_prices.total)}")

    def validate_both_consumptions_have_same_buckets(self) -> None:
        for bucket in self.data.hourly.buckets.values():
            if bucket.consumption_kwh.total is None:
                raise MismatchedBucketsException(f"Hourly bucket missing value for total consumption, hour={bucket.start}")
            if bucket.consumption_kwh.heat_pump is None:
                raise MismatchedBucketsException(f"Hourly bucket missing value for heat pump consumption, hour={bucket.start}")

    def increase_total_consumption_when_heat_pump_consumption_is_greater_than_total_consumption(self):
        fixed_hours = []
        for bucket in self.data.hourly.buckets.values():
            if bucket.consumption_kwh.heat_pump > bucket.consumption_kwh.total:
                self.data.hourly.set_total_consumption(bucket.start, bucket.consumption_kwh.heat_pump)
                fixed_hours.append(bucket.start)

        if len(fixed_hours) > 0:
            print("**** Warning ****")
            print(f"The following {len(fixed_hours)} hourly buckets had greater heat pump consumption than total consumption.")
            print("This has been fixed by copying the heat pump consumption value into the total consumption value.")
            for fixed_hour in fixed_hours:
                print(f"- {fixed_hour}")
            print()
