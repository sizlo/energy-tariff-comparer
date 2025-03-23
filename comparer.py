from tariff_price_writer import TariffPriceWriter
from consumption import Consumption
from consumption_price import ConsumptionPrice
from consumption_price_calculator import ConsumptionPriceCalculator
from exception import MismatchedBucketsException
from tariff import Tariff
from tarrif_price import TariffPrice
from util import render_price


class Comparer:
    def __init__(self, heat_pump_consumption: Consumption, total_consumption: Consumption, tariffs: [Tariff]):
        self.heat_pump_consumption = heat_pump_consumption
        self.total_consumption = total_consumption
        self.tariffs = tariffs

        self.validate_both_consumptions_have_same_buckets()
        self.increase_total_consumption_when_heat_pump_consumption_is_greater_than_total_consumption()

    def compare(self, output_csvs: bool = False) -> None:
        tariff_prices = [TariffPrice(tariff, self.get_price(tariff)) for tariff in self.tariffs]
        tariff_prices.sort(key=lambda tp: tp.consumption_price.total_price_pence)

        # TODO - control writing csvs from cli options
        if output_csvs:
            TariffPriceWriter(tariff_prices, "TODO").write()

        print("**** Total price for entire period of input data for each tariff ****")
        for tariff_price in tariff_prices:
            print(f"{tariff_price.tariff.name}: {render_price(tariff_price.consumption_price.total_price_pence)}")

    def validate_both_consumptions_have_same_buckets(self) -> None:
        for total_key in self.total_consumption.buckets.keys():
            if total_key not in self.heat_pump_consumption.buckets.keys():
                raise MismatchedBucketsException(f"Bucket is present in total_consumption, but not in heat_pump_consumption, bucket={total_key}")

        for heat_pump_key in self.heat_pump_consumption.buckets.keys():
            if heat_pump_key not in self.total_consumption.buckets.keys():
                raise MismatchedBucketsException(f"Bucket is present in heat_pump_consumption, but not in total_consumption, bucket={heat_pump_key}")

    def increase_total_consumption_when_heat_pump_consumption_is_greater_than_total_consumption(self):
        fixed_hours = []
        for hour in self.total_consumption.buckets.keys():
            hourly_heat_pump_consumption = self.heat_pump_consumption.buckets[hour]
            hourly_total_consumption = self.total_consumption.buckets[hour]
            if hourly_heat_pump_consumption > hourly_total_consumption:
                self.total_consumption.buckets[hour] = hourly_heat_pump_consumption
                fixed_hours.append(hour)
        if len(fixed_hours) > 0:
            print("**** Warning ****")
            print(f"The following {len(fixed_hours)} buckets had greater heat pump consumption than total consumption.")
            print("This has been fixed by copying the heat pump consumption value into the total consumption bucket.")
            for fixed_hour in fixed_hours:
                print(f"- {fixed_hour}")
            print()

    def get_price(self, tariff: Tariff) -> ConsumptionPrice:
        calculator = ConsumptionPriceCalculator(self.heat_pump_consumption, self.total_consumption, tariff)
        return calculator.calculate_consumption_price()
