import unittest
from datetime import datetime

from data import Data
from hourly_price_calculator import HourlyPriceCalculator
from tariff import StandardTariff, FlatHeatPumpRateTariff, HourlyVariableTariff


class HourlyPriceCalculatorTests(unittest.TestCase):
    def setUp(self):
        self.hour = datetime(2025, 3, 12, 4)
        self.dhw_consumption = 1
        self.heating_consumption = 2
        self.total_consumption = 7

        self.data = Data()
        self.data.hourly.set_heat_pump_consumption(self.hour, self.dhw_consumption, self.heating_consumption)
        self.data.hourly.set_total_consumption(self.hour, self.total_consumption)

    def test_calculates_prices_with_standard_tariff(self):
        tariff = StandardTariff("standard", 0, 3)

        calculator = HourlyPriceCalculator(self.data, tariff)
        calculator.calculate()

        self.assertEqual(3, self.data.hourly.at_start(self.hour).tariff_prices_pence["standard"].dhw)
        self.assertEqual(6, self.data.hourly.at_start(self.hour).tariff_prices_pence["standard"].heating)
        self.assertEqual(9, self.data.hourly.at_start(self.hour).tariff_prices_pence["standard"].heat_pump)
        self.assertEqual(12, self.data.hourly.at_start(self.hour).tariff_prices_pence["standard"].non_heat_pump)
        self.assertEqual(21, self.data.hourly.at_start(self.hour).tariff_prices_pence["standard"].total)

    def test_calculates_prices_with_flat_heat_pump_rate_tariff(self):
        tariff = FlatHeatPumpRateTariff("flat-heat-pump-rate", 0, 2, 5)

        calculator = HourlyPriceCalculator(self.data, tariff)
        calculator.calculate()

        self.assertEqual(2, self.data.hourly.at_start(self.hour).tariff_prices_pence["flat-heat-pump-rate"].dhw)
        self.assertEqual(4, self.data.hourly.at_start(self.hour).tariff_prices_pence["flat-heat-pump-rate"].heating)
        self.assertEqual(6, self.data.hourly.at_start(self.hour).tariff_prices_pence["flat-heat-pump-rate"].heat_pump)
        self.assertEqual(20, self.data.hourly.at_start(self.hour).tariff_prices_pence["flat-heat-pump-rate"].non_heat_pump)
        self.assertEqual(26, self.data.hourly.at_start(self.hour).tariff_prices_pence["flat-heat-pump-rate"].total)

    def test_calculates_prices_with_hourly_variable_tariff(self):
        tariff = HourlyVariableTariff(
            "hourly-variable",
            0,
            {
                self.hour.hour: 7
            }
        )

        calculator = HourlyPriceCalculator(self.data, tariff)
        calculator.calculate()

        self.assertEqual(7, self.data.hourly.at_start(self.hour).tariff_prices_pence["hourly-variable"].dhw)
        self.assertEqual(14, self.data.hourly.at_start(self.hour).tariff_prices_pence["hourly-variable"].heating)
        self.assertEqual(21, self.data.hourly.at_start(self.hour).tariff_prices_pence["hourly-variable"].heat_pump)
        self.assertEqual(28, self.data.hourly.at_start(self.hour).tariff_prices_pence["hourly-variable"].non_heat_pump)
        self.assertEqual(49, self.data.hourly.at_start(self.hour).tariff_prices_pence["hourly-variable"].total)
