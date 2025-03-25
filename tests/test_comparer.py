import unittest
from datetime import datetime

from comparer import Comparer
from data import Data
from exception import MismatchedBucketsException
from tariff import StandardTariff


class ComparerTests(unittest.TestCase):
    def test_errors_if_heat_pump_consumption_is_missing_a_bucket_which_is_present_in_total_consumption(self):
        data = Data()

        data.hourly.set_heat_pump_consumption(datetime(2025, 3, 23, 5), 1, 11)
        data.hourly.set_heat_pump_consumption(datetime(2025, 3, 23, 7), 3, 33)

        data.hourly.set_total_consumption(datetime(2025, 3, 23, 5), 444)
        data.hourly.set_total_consumption(datetime(2025, 3, 23, 6), 555)
        data.hourly.set_total_consumption(datetime(2025, 3, 23, 7), 666)

        tariff = StandardTariff("standard", 0.1, 0.2)

        with self.assertRaises(MismatchedBucketsException):
            Comparer(data, [tariff])

    def test_errors_if_total_consumption_is_missing_a_bucket_which_is_present_in_heat_pump_consumption(self):
        data = Data()

        data.hourly.set_heat_pump_consumption(datetime(2025, 3, 23, 5), 1, 11)
        data.hourly.set_heat_pump_consumption(datetime(2025, 3, 23, 6), 2, 22)
        data.hourly.set_heat_pump_consumption(datetime(2025, 3, 23, 7), 3, 33)

        data.hourly.set_total_consumption(datetime(2025, 3, 23, 5), 444)
        data.hourly.set_total_consumption(datetime(2025, 3, 23, 7), 666)

        tariff = StandardTariff("standard", 0.1, 0.2)

        with self.assertRaises(MismatchedBucketsException):
            Comparer(data, [tariff])

    def test_increases_total_consumption_when_heat_pump_consumption_is_greater_than_total_consumption(self):
        data = Data()

        data.hourly.set_heat_pump_consumption(datetime(2025, 3, 23, 5), 1, 11)
        data.hourly.set_heat_pump_consumption(datetime(2025, 3, 23, 6), 7, 770)
        data.hourly.set_heat_pump_consumption(datetime(2025, 3, 23, 7), 3, 33)

        data.hourly.set_total_consumption(datetime(2025, 3, 23, 5), 444)
        data.hourly.set_total_consumption(datetime(2025, 3, 23, 6), 555)
        data.hourly.set_total_consumption(datetime(2025, 3, 23, 7), 666)

        tariff = StandardTariff("standard", 0.1, 0.2)

        Comparer(data, [tariff])

        self.assertEqual(777, data.hourly.at_start(datetime(2025, 3, 23, 6)).consumption_kwh.total)
