import unittest
from datetime import datetime

from comparer import Comparer
from consumption import Consumption
from exception import MismatchedBucketsException
from tariff import StandardTariff


class ComparerTests(unittest.TestCase):
    def test_errors_if_heat_pump_consumption_is_missing_a_bucket_which_is_present_in_total_consumption(self):
        heat_pump_consumption = Consumption(
            "heat pump",
            {
                datetime(2025, 3, 23, 5): 111,
                datetime(2025, 3, 23, 7): 333,
            }
        )

        total_consumption = Consumption(
            "total",
            {
                datetime(2025, 3, 23, 5): 444,
                datetime(2025, 3, 23, 6): 555,
                datetime(2025, 3, 23, 7): 666,
            }
        )

        tariff = StandardTariff("standard", 0.1, 0.2)

        with self.assertRaises(MismatchedBucketsException):
            Comparer(heat_pump_consumption, total_consumption, [tariff])

    def test_errors_if_total_consumption_is_missing_a_bucket_which_is_present_in_heat_pump_consumption(self):
        heat_pump_consumption = Consumption(
            "heat pump",
            {
                datetime(2025, 3, 23, 5): 111,
                datetime(2025, 3, 23, 6): 222,
                datetime(2025, 3, 23, 7): 333,
            }
        )

        total_consumption = Consumption(
            "total",
            {
                datetime(2025, 3, 23, 5): 444,
                datetime(2025, 3, 23, 7): 666,
            }
        )

        tariff = StandardTariff("standard", 0.1, 0.2)

        with self.assertRaises(MismatchedBucketsException):
            Comparer(heat_pump_consumption, total_consumption, [tariff])

    def test_increases_total_consumption_when_heat_pump_consumption_is_greater_than_total_consumption(self):
        heat_pump_consumption = Consumption(
            "heat pump",
            {
                datetime(2025, 3, 23, 5): 111,
                datetime(2025, 3, 23, 6): 777,
                datetime(2025, 3, 23, 7): 333,
            }
        )

        total_consumption = Consumption(
            "total",
            {
                datetime(2025, 3, 23, 5): 444,
                datetime(2025, 3, 23, 6): 555,
                datetime(2025, 3, 23, 7): 666,
            }
        )

        tariff = StandardTariff("standard", 0.1, 0.2)

        comparer = Comparer(heat_pump_consumption, total_consumption, [tariff])

        self.assertEqual(777, comparer.total_consumption.buckets[datetime(2025, 3, 23, 6)])
