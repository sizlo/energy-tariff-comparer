from data import Data, TariffPrices
from tariff import Tariff


class HourlyPriceCalculator:
    def __init__(self, data: Data, tariff: Tariff):
        self.data = data
        self.tariff = tariff

    def calculate(self):
        for bucket_data in self.data.hourly.buckets.values():
            tariff_prices = TariffPrices(self.tariff)
            tariff_prices.dhw = self.tariff.get_price_in_pence_for_hourly_heat_pump_use(bucket_data.start, bucket_data.consumption_kwh.dhw)
            tariff_prices.heating = self.tariff.get_price_in_pence_for_hourly_heat_pump_use(bucket_data.start, bucket_data.consumption_kwh.heating)
            tariff_prices.heat_pump = self.tariff.get_price_in_pence_for_hourly_heat_pump_use(bucket_data.start, bucket_data.consumption_kwh.heat_pump)
            tariff_prices.non_heat_pump = self.tariff.get_price_in_pence_for_hourly_heat_pump_use(bucket_data.start, bucket_data.consumption_kwh.non_heat_pump)
            tariff_prices.total = self.tariff.get_price_in_pence_for_hourly_heat_pump_use(bucket_data.start, bucket_data.consumption_kwh.total)
            bucket_data.tariff_prices_pence[self.tariff.name] = tariff_prices
