import unittest
import os
from datetime import datetime

from vaillant_parser import VaillantParser

TEST_DATA = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "vaillant")


class VaillantParserTests(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = VaillantParser()

    def test_source_is_vaillant(self) -> None:
        consumption = self.parser.parse(os.path.join(TEST_DATA, "valid.csv"))
        self.assertEqual("vaillant", consumption.source)

    def test_gets_correct_count_of_buckets(self) -> None:
        consumption = self.parser.parse(os.path.join(TEST_DATA, "valid.csv"))
        self.assertEqual(48, len(consumption.buckets))

    def test_bucket_values_are_sum_of_dhw_and_heating_usage_converted_to_kwh(self) -> None:
        consumption = self.parser.parse(os.path.join(TEST_DATA, "valid.csv"))
        self.assertAlmostEqual(0.5234340052816901, consumption.buckets[datetime(2025, 2, 11, 0)])
        self.assertAlmostEqual(0.6798820884683099, consumption.buckets[datetime(2025, 2, 11, 1)])
        self.assertAlmostEqual(0.5674215042483268, consumption.buckets[datetime(2025, 2, 11, 2)])
        self.assertAlmostEqual(0.84224075937, consumption.buckets[datetime(2025, 2, 11, 7)])
        self.assertAlmostEqual(1.11205876759, consumption.buckets[datetime(2025, 2, 11, 8)])
        self.assertAlmostEqual(1.43101068565, consumption.buckets[datetime(2025, 2, 11, 9)])
        self.assertAlmostEqual(0.4977575153212172, consumption.buckets[datetime(2025, 2, 11, 22)])
        self.assertAlmostEqual(0.4160746555144476, consumption.buckets[datetime(2025, 2, 11, 23)])
        self.assertAlmostEqual(0.4051547657790927, consumption.buckets[datetime(2025, 2, 12, 0)])
        self.assertAlmostEqual(0.50407810269105653, consumption.buckets[datetime(2025, 2, 12, 1)])
        self.assertAlmostEqual(0.5142208331138825, consumption.buckets[datetime(2025, 2, 12, 21)])
        self.assertAlmostEqual(0.38658080963103794, consumption.buckets[datetime(2025, 2, 12, 22)])
        self.assertAlmostEqual(0.32021549619682673, consumption.buckets[datetime(2025, 2, 12, 23)])

    def test_errors_if_start_is_not_exact_hour_time(self) -> None:
        with self.assertRaises(Exception):
            self.parser.parse(os.path.join(TEST_DATA, "start_is_not_exact_hour_time.csv"))

    def test_errors_if_end_is_not_exact_hour_time(self) -> None:
        with self.assertRaises(Exception):
            self.parser.parse(os.path.join(TEST_DATA, "end_is_not_exact_hour_time.csv"))

    def test_errors_if_end_is_not_exactly_one_hour_after_start(self) -> None:
        with self.assertRaises(Exception):
            self.parser.parse(os.path.join(TEST_DATA, "end_is_not_exactly_one_hour_after_start.csv"))

    def test_errors_if_hourly_bucket_is_missing(self) -> None:
        with self.assertRaises(Exception):
            self.parser.parse(os.path.join(TEST_DATA, "missing_hourly_bucket.csv"))