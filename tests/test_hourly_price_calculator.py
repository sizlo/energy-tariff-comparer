import unittest
from datetime import datetime

from data import Data
from hourly_price_calculator import HourlyPriceCalculator
from tariff import StandardTariff


class HourlyPriceCalculatorTests(unittest.TestCase):
    def setUp(self):
        self.hour = datetime(2025, 3, 12, 4)
        self.dhw_consumption = 1
        self.heating_consumption = 2
        self.total_consumption = 7

        self.data = Data()
        self.data.hourly.set_heat_pump_consumption(self.hour, self.dhw_consumption, self.heating_consumption)
        self.data.hourly.set_total_consumption(self.hour, self.total_consumption)

        self.tariff = StandardTariff("tariff-name", 0, 3)

        self.calculator = HourlyPriceCalculator(self.data, self.tariff)

    def test_calculates_prices(self):
        self.calculator.calculate()
        self.assertEqual(3, self.data.hourly.at_start(self.hour).tariff_prices_pence["tariff-name"].dhw)
        self.assertEqual(6, self.data.hourly.at_start(self.hour).tariff_prices_pence["tariff-name"].heating)
        self.assertEqual(9, self.data.hourly.at_start(self.hour).tariff_prices_pence["tariff-name"].heat_pump)
        self.assertEqual(12, self.data.hourly.at_start(self.hour).tariff_prices_pence["tariff-name"].non_heat_pump)
        self.assertEqual(21, self.data.hourly.at_start(self.hour).tariff_prices_pence["tariff-name"].total)
