import unittest
from datetime import datetime

from tariff import StandardTariff, HourlyVariableTariff, FlatHeatPumpRateTariff


class StandardTariffTests(unittest.TestCase):
    def test_multiplies_combined_hourly_usage_by_unit_rate(self):
        unit_rate = 123.45
        tariff = StandardTariff("test", 0.0, unit_rate)

        heat_pump_hourly_usage = 321.45
        non_heat_pump_hourly_usage = 856.33

        result = tariff.get_price_in_pence_for_hourly_use(datetime.now(), heat_pump_hourly_usage, non_heat_pump_hourly_usage)
        self.assertEqual(145396.941, result)


class HourlyVariableTariffTests(unittest.TestCase):
    def test_multiplies_combined_hourly_usage_by_this_hours_unit_rate(self):
        hourly_unit_rates = {
            0: 1.23,
            1: 2.64,
            2: 5.26,
            3: 3.86,
            4: 3.27,
            5: 8.24,
            6: 6.39,
            7: 8.36,
            8: 4.75,
            9: 5.67,
            10: 4.78,
            11: 4.56,
            12: 7.48,
            13: 8.90,
            14: 0.34,
            15: 5.74,
            16: 2.22,
            17: 4.74,
            18: 5.80,
            19: 0.48,
            21: 1.54,
            22: 7.99,
            23: 9.14
        }
        self.tariff = HourlyVariableTariff("test", 0.0, hourly_unit_rates)

        self.assertHourlyPriceIs(expected=7.4415, hour=0, heat_pump_usage=2.68, non_heat_pump_usage=3.37)
        self.assertHourlyPriceIs(expected=24.3936, hour=1, heat_pump_usage=2.95, non_heat_pump_usage=6.29)
        self.assertHourlyPriceIs(expected=37.8720, hour=2, heat_pump_usage=5.47, non_heat_pump_usage=1.73)
        self.assertHourlyPriceIs(expected=21.5774, hour=3, heat_pump_usage=0.68, non_heat_pump_usage=4.91)
        self.assertHourlyPriceIs(expected=25.1463, hour=4, heat_pump_usage=4.02, non_heat_pump_usage=3.67)
        self.assertHourlyPriceIs(expected=83.0592, hour=5, heat_pump_usage=3.03, non_heat_pump_usage=7.05)
        self.assertHourlyPriceIs(expected=99.8757, hour=6, heat_pump_usage=6.41, non_heat_pump_usage=9.22)
        self.assertHourlyPriceIs(expected=130.0816, hour=7, heat_pump_usage=7.76, non_heat_pump_usage=7.80)
        self.assertHourlyPriceIs(expected=28.7850, hour=8, heat_pump_usage=5.80, non_heat_pump_usage=0.26)
        self.assertHourlyPriceIs(expected=51.5970, hour=9, heat_pump_usage=0.44, non_heat_pump_usage=8.66)
        self.assertHourlyPriceIs(expected=56.4518, hour=10, heat_pump_usage=3.58, non_heat_pump_usage=8.23)
        self.assertHourlyPriceIs(expected=54.3552, hour=11, heat_pump_usage=8.77, non_heat_pump_usage=3.15)
        self.assertHourlyPriceIs(expected=45.0296, hour=12, heat_pump_usage=5.62, non_heat_pump_usage=0.40)
        self.assertHourlyPriceIs(expected=88.644, hour=13, heat_pump_usage=2.77, non_heat_pump_usage=7.19)
        self.assertHourlyPriceIs(expected=5.52160, hour=14, heat_pump_usage=6.44, non_heat_pump_usage=9.80)
        self.assertHourlyPriceIs(expected=41.2132, hour=15, heat_pump_usage=6.76, non_heat_pump_usage=0.42)
        self.assertHourlyPriceIs(expected=30.8802, hour=16, heat_pump_usage=7.90, non_heat_pump_usage=6.01)
        self.assertHourlyPriceIs(expected=74.1810, hour=17, heat_pump_usage=6.75, non_heat_pump_usage=8.90)
        self.assertHourlyPriceIs(expected=36.018, hour=18, heat_pump_usage=5.85, non_heat_pump_usage=0.36)
        self.assertHourlyPriceIs(expected=5.568, hour=19, heat_pump_usage=8.35, non_heat_pump_usage=3.25)

    def assertHourlyPriceIs(self, expected: float, hour: int, heat_pump_usage: float, non_heat_pump_usage: float) -> None:
        date = date_at_hour(hour)
        price = self.tariff.get_price_in_pence_for_hourly_use(date, heat_pump_usage, non_heat_pump_usage)
        self.assertAlmostEqual(expected, price)


class FlatHeatPumpRateTariffTests(unittest.TestCase):
    def test_price_is_sum_of_heat_pump_usage_multiplied_by_heat_pump_rate_and_non_heat_pump_usage_multiplied_by_non_heat_pump_rate(self):
        heat_pump_unit_rate = 123.45
        non_heat_pump_unit_rate = 578.23
        tariff = FlatHeatPumpRateTariff("test", 0.0, heat_pump_unit_rate, non_heat_pump_unit_rate)

        heat_pump_hourly_usage = 321.45
        non_heat_pump_hourly_usage = 856.33

        result = tariff.get_price_in_pence_for_hourly_use(datetime.now(), heat_pump_hourly_usage, non_heat_pump_hourly_usage)
        self.assertAlmostEqual(534838.6984, result)


def date_at_hour(hour: int) -> datetime:
    return datetime(2025, 3, 23, hour)