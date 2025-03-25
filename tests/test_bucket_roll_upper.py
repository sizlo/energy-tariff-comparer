import unittest
from datetime import datetime

from data import Data
from hourly_price_calculator import HourlyPriceCalculator
from tariff import StandardTariff
from bucket_roll_upper import BucketRollUpper


class BucketRollUpperTests(unittest.TestCase):
    def setUp(self):
        self.data = Data()

    def test_rolls_up(self):
        self.add_hourly_consumptions(datetime(2022, 12, 5, 6), 12, 56, 102)
        self.add_hourly_consumptions(datetime(2023, 1, 5, 13), 85, 8, 456)
        self.add_hourly_consumptions(datetime(2023, 1, 5, 14), 27, 2, 156)
        self.add_hourly_consumptions(datetime(2023, 1, 5, 15), 34, 3, 134)
        self.add_hourly_consumptions(datetime(2023, 1, 8, 9), 60, 23, 99)
        self.add_hourly_consumptions(datetime(2023, 6, 2, 4), 9, 3, 45)
        self.add_hourly_consumptions(datetime(2023, 7, 5, 9), 5, 39, 145)
        self.add_hourly_consumptions(datetime(2024, 1, 8, 9), 12, 21, 50)

        HourlyPriceCalculator(self.data, StandardTariff("one", 4, 6)).calculate()
        HourlyPriceCalculator(self.data, StandardTariff("two", 23, 5)).calculate()

        BucketRollUpper(self.data).roll_up()

        self.assertEqual(146, self.data.daily.at_start(datetime(2023, 1, 5)).consumption_kwh.dhw)
        self.assertEqual(13, self.data.daily.at_start(datetime(2023, 1, 5)).consumption_kwh.heating)
        self.assertEqual(159, self.data.daily.at_start(datetime(2023, 1, 5)).consumption_kwh.heat_pump)
        self.assertEqual(587, self.data.daily.at_start(datetime(2023, 1, 5)).consumption_kwh.non_heat_pump)
        self.assertEqual(746, self.data.daily.at_start(datetime(2023, 1, 5)).consumption_kwh.total)

        self.assertEqual(876, self.data.daily.at_start(datetime(2023, 1, 5)).tariff_prices_pence["one"].dhw)
        self.assertEqual(78, self.data.daily.at_start(datetime(2023, 1, 5)).tariff_prices_pence["one"].heating)
        self.assertEqual(954, self.data.daily.at_start(datetime(2023, 1, 5)).tariff_prices_pence["one"].heat_pump)
        self.assertEqual(3522, self.data.daily.at_start(datetime(2023, 1, 5)).tariff_prices_pence["one"].non_heat_pump)
        self.assertEqual(4, self.data.daily.at_start(datetime(2023, 1, 5)).tariff_prices_pence["one"].standing_charge)
        self.assertEqual(4480, self.data.daily.at_start(datetime(2023, 1, 5)).tariff_prices_pence["one"].total)

        self.assertEqual(730, self.data.daily.at_start(datetime(2023, 1, 5)).tariff_prices_pence["two"].dhw)
        self.assertEqual(65, self.data.daily.at_start(datetime(2023, 1, 5)).tariff_prices_pence["two"].heating)
        self.assertEqual(795, self.data.daily.at_start(datetime(2023, 1, 5)).tariff_prices_pence["two"].heat_pump)
        self.assertEqual(2935, self.data.daily.at_start(datetime(2023, 1, 5)).tariff_prices_pence["two"].non_heat_pump)
        self.assertEqual(23, self.data.daily.at_start(datetime(2023, 1, 5)).tariff_prices_pence["two"].standing_charge)
        self.assertEqual(3753, self.data.daily.at_start(datetime(2023, 1, 5)).tariff_prices_pence["two"].total)

        self.assertEqual(206, self.data.monthly.at_start(datetime(2023, 1, 1)).consumption_kwh.dhw)
        self.assertEqual(36, self.data.monthly.at_start(datetime(2023, 1, 1)).consumption_kwh.heating)
        self.assertEqual(242, self.data.monthly.at_start(datetime(2023, 1, 1)).consumption_kwh.heat_pump)
        self.assertEqual(603, self.data.monthly.at_start(datetime(2023, 1, 1)).consumption_kwh.non_heat_pump)
        self.assertEqual(845, self.data.monthly.at_start(datetime(2023, 1, 1)).consumption_kwh.total)

        self.assertEqual(1236, self.data.monthly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["one"].dhw)
        self.assertEqual(216, self.data.monthly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["one"].heating)
        self.assertEqual(1452, self.data.monthly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["one"].heat_pump)
        self.assertEqual(3618, self.data.monthly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["one"].non_heat_pump)
        self.assertEqual(8, self.data.monthly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["one"].standing_charge)
        self.assertEqual(5078, self.data.monthly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["one"].total)

        self.assertEqual(1030, self.data.monthly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["two"].dhw)
        self.assertEqual(180, self.data.monthly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["two"].heating)
        self.assertEqual(1210, self.data.monthly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["two"].heat_pump)
        self.assertEqual(3015, self.data.monthly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["two"].non_heat_pump)
        self.assertEqual(46, self.data.monthly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["two"].standing_charge)
        self.assertEqual(4271, self.data.monthly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["two"].total)

        self.assertEqual(220, self.data.yearly.at_start(datetime(2023, 1, 1)).consumption_kwh.dhw)
        self.assertEqual(78, self.data.yearly.at_start(datetime(2023, 1, 1)).consumption_kwh.heating)
        self.assertEqual(298, self.data.yearly.at_start(datetime(2023, 1, 1)).consumption_kwh.heat_pump)
        self.assertEqual(737, self.data.yearly.at_start(datetime(2023, 1, 1)).consumption_kwh.non_heat_pump)
        self.assertEqual(1035, self.data.yearly.at_start(datetime(2023, 1, 1)).consumption_kwh.total)

        self.assertEqual(1320, self.data.yearly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["one"].dhw)
        self.assertEqual(468, self.data.yearly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["one"].heating)
        self.assertEqual(1788, self.data.yearly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["one"].heat_pump)
        self.assertEqual(4422, self.data.yearly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["one"].non_heat_pump)
        self.assertEqual(16, self.data.yearly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["one"].standing_charge)
        self.assertEqual(6226, self.data.yearly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["one"].total)

        self.assertEqual(1100, self.data.yearly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["two"].dhw)
        self.assertEqual(390, self.data.yearly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["two"].heating)
        self.assertEqual(1490, self.data.yearly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["two"].heat_pump)
        self.assertEqual(3685, self.data.yearly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["two"].non_heat_pump)
        self.assertEqual(92, self.data.yearly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["two"].standing_charge)
        self.assertEqual(5267, self.data.yearly.at_start(datetime(2023, 1, 1)).tariff_prices_pence["two"].total)

        self.assertEqual(244, self.data.total.consumption_kwh.dhw)
        self.assertEqual(155, self.data.total.consumption_kwh.heating)
        self.assertEqual(399, self.data.total.consumption_kwh.heat_pump)
        self.assertEqual(788, self.data.total.consumption_kwh.non_heat_pump)
        self.assertEqual(1187, self.data.total.consumption_kwh.total)

        self.assertEqual(1464, self.data.total.tariff_prices_pence["one"].dhw)
        self.assertEqual(930, self.data.total.tariff_prices_pence["one"].heating)
        self.assertEqual(2394, self.data.total.tariff_prices_pence["one"].heat_pump)
        self.assertEqual(4728, self.data.total.tariff_prices_pence["one"].non_heat_pump)
        self.assertEqual(24, self.data.total.tariff_prices_pence["one"].standing_charge)
        self.assertEqual(7146, self.data.total.tariff_prices_pence["one"].total)

        self.assertEqual(1220, self.data.total.tariff_prices_pence["two"].dhw)
        self.assertEqual(775, self.data.total.tariff_prices_pence["two"].heating)
        self.assertEqual(1995, self.data.total.tariff_prices_pence["two"].heat_pump)
        self.assertEqual(3940, self.data.total.tariff_prices_pence["two"].non_heat_pump)
        self.assertEqual(138, self.data.total.tariff_prices_pence["two"].standing_charge)
        self.assertEqual(6073, self.data.total.tariff_prices_pence["two"].total)

    def add_hourly_consumptions(self, hour, dhw, heating, total):
        self.data.hourly.set_heat_pump_consumption(hour, dhw, heating)
        self.data.hourly.set_total_consumption(hour, total)
