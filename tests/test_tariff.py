import unittest
from datetime import datetime

from tariff import StandardTariff, HourlyVariableTariff, FlatHeatPumpRateTariff


class StandardTariffTests(unittest.TestCase):
    def test_multiplies_usage_by_unit_rate(self):
        unit_rate = 123.45
        tariff = StandardTariff("test", 0.0, unit_rate)

        heat_pump_hourly_usage = 321.45
        non_heat_pump_hourly_usage = 856.33

        heat_pump_price = tariff.get_price_in_pence_for_hourly_heat_pump_use(datetime.now(), heat_pump_hourly_usage)
        self.assertEqual(39683.0025, heat_pump_price)

        non_heat_pump_price = tariff.get_price_in_pence_for_hourly_non_heat_pump_use(datetime.now(), non_heat_pump_hourly_usage)
        self.assertEqual(105713.9385, non_heat_pump_price)


class HourlyVariableTariffTests(unittest.TestCase):
    def test_multiplies_hourly_usage_by_this_hours_unit_rate(self):
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

        self.assertHourlyPriceIs(expected_heat_pump_price=3.2964, expected_non_heat_pump_price=4.1451, hour=0, heat_pump_usage=2.68, non_heat_pump_usage=3.37)
        self.assertHourlyPriceIs(expected_heat_pump_price=7.788, expected_non_heat_pump_price=16.6056, hour=1, heat_pump_usage=2.95, non_heat_pump_usage=6.29)
        self.assertHourlyPriceIs(expected_heat_pump_price=28.7722, expected_non_heat_pump_price=9.0998, hour=2, heat_pump_usage=5.47, non_heat_pump_usage=1.73)
        self.assertHourlyPriceIs(expected_heat_pump_price=2.6248, expected_non_heat_pump_price=18.9526, hour=3, heat_pump_usage=0.68, non_heat_pump_usage=4.91)
        self.assertHourlyPriceIs(expected_heat_pump_price=13.1454, expected_non_heat_pump_price=12.0009, hour=4, heat_pump_usage=4.02, non_heat_pump_usage=3.67)
        self.assertHourlyPriceIs(expected_heat_pump_price=24.9672, expected_non_heat_pump_price=58.092, hour=5, heat_pump_usage=3.03, non_heat_pump_usage=7.05)
        self.assertHourlyPriceIs(expected_heat_pump_price=40.9599, expected_non_heat_pump_price=58.9158, hour=6, heat_pump_usage=6.41, non_heat_pump_usage=9.22)
        self.assertHourlyPriceIs(expected_heat_pump_price=64.8736, expected_non_heat_pump_price=65.208, hour=7, heat_pump_usage=7.76, non_heat_pump_usage=7.80)
        self.assertHourlyPriceIs(expected_heat_pump_price=27.55, expected_non_heat_pump_price=1.235, hour=8, heat_pump_usage=5.80, non_heat_pump_usage=0.26)
        self.assertHourlyPriceIs(expected_heat_pump_price=2.4948, expected_non_heat_pump_price=49.1022, hour=9, heat_pump_usage=0.44, non_heat_pump_usage=8.66)
        self.assertHourlyPriceIs(expected_heat_pump_price=17.1124, expected_non_heat_pump_price=39.3394, hour=10, heat_pump_usage=3.58, non_heat_pump_usage=8.23)
        self.assertHourlyPriceIs(expected_heat_pump_price=39.9912, expected_non_heat_pump_price=14.364, hour=11, heat_pump_usage=8.77, non_heat_pump_usage=3.15)
        self.assertHourlyPriceIs(expected_heat_pump_price=42.0376, expected_non_heat_pump_price=2.992, hour=12, heat_pump_usage=5.62, non_heat_pump_usage=0.40)
        self.assertHourlyPriceIs(expected_heat_pump_price=24.6530, expected_non_heat_pump_price=63.991, hour=13, heat_pump_usage=2.77, non_heat_pump_usage=7.19)
        self.assertHourlyPriceIs(expected_heat_pump_price=2.1896, expected_non_heat_pump_price=3.332, hour=14, heat_pump_usage=6.44, non_heat_pump_usage=9.80)
        self.assertHourlyPriceIs(expected_heat_pump_price=38.8024, expected_non_heat_pump_price=2.4108, hour=15, heat_pump_usage=6.76, non_heat_pump_usage=0.42)
        self.assertHourlyPriceIs(expected_heat_pump_price=17.538, expected_non_heat_pump_price=13.3422, hour=16, heat_pump_usage=7.90, non_heat_pump_usage=6.01)
        self.assertHourlyPriceIs(expected_heat_pump_price=31.995, expected_non_heat_pump_price=42.186, hour=17, heat_pump_usage=6.75, non_heat_pump_usage=8.90)
        self.assertHourlyPriceIs(expected_heat_pump_price=33.93, expected_non_heat_pump_price=2.088, hour=18, heat_pump_usage=5.85, non_heat_pump_usage=0.36)
        self.assertHourlyPriceIs(expected_heat_pump_price=4.008, expected_non_heat_pump_price=1.56, hour=19, heat_pump_usage=8.35, non_heat_pump_usage=3.25)

    def assertHourlyPriceIs(self, expected_heat_pump_price: float, expected_non_heat_pump_price: float, hour: int, heat_pump_usage: float, non_heat_pump_usage: float) -> None:
        date = date_at_hour(hour)

        heat_pump_price = self.tariff.get_price_in_pence_for_hourly_heat_pump_use(date, heat_pump_usage)
        self.assertAlmostEqual(expected_heat_pump_price, heat_pump_price)

        non_heat_pump_price = self.tariff.get_price_in_pence_for_hourly_non_heat_pump_use(date, non_heat_pump_usage)
        self.assertAlmostEqual(expected_non_heat_pump_price, non_heat_pump_price)


class FlatHeatPumpRateTariffTests(unittest.TestCase):
    def test_heat_pump_price_is_usage_multiplied_by_heat_pump_rate_and_non_heat_pump_price_is_usage_multiplied_by_non_heat_pump_rate(self):
        heat_pump_unit_rate = 123.45
        non_heat_pump_unit_rate = 578.23
        tariff = FlatHeatPumpRateTariff("test", 0.0, heat_pump_unit_rate, non_heat_pump_unit_rate)

        heat_pump_hourly_usage = 321.45
        heat_pump_price = tariff.get_price_in_pence_for_hourly_heat_pump_use(datetime.now(), heat_pump_hourly_usage)
        self.assertEqual(heat_pump_price, 39683.0025)

        non_heat_pump_hourly_usage = 856.33
        non_heat_pump_price = tariff.get_price_in_pence_for_hourly_non_heat_pump_use(datetime.now(), non_heat_pump_hourly_usage)
        self.assertAlmostEqual(495155.6959, non_heat_pump_price)


def date_at_hour(hour: int) -> datetime:
    return datetime(2025, 3, 23, hour)