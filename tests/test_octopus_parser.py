import unittest
import os
from datetime import datetime

from exception import ParserException
from octopus_parser import OctopusParser

TEST_DATA = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "octopus")


class OctopusParserTests(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = OctopusParser()

    def test_source_is_octopus(self) -> None:
        consumption = self.parser.parse(os.path.join(TEST_DATA, "valid.csv"))
        self.assertEqual("octopus", consumption.source)

    def test_gets_correct_count_of_buckets(self) -> None:
        consumption = self.parser.parse(os.path.join(TEST_DATA, "valid.csv"))
        self.assertEqual(48, len(consumption.buckets))

    def test_bucket_values_are_sum_of_each_half_hour_within_hour(self) -> None:
        consumption = self.parser.parse(os.path.join(TEST_DATA, "valid.csv"))
        self.assertAlmostEqual(0.691, consumption.buckets[datetime(2025, 2, 11, 0)])
        self.assertAlmostEqual(0.829, consumption.buckets[datetime(2025, 2, 11, 1)])
        self.assertAlmostEqual(0.665, consumption.buckets[datetime(2025, 2, 11, 2)])
        self.assertAlmostEqual(0.457, consumption.buckets[datetime(2025, 2, 11, 22)])
        self.assertAlmostEqual(0.752, consumption.buckets[datetime(2025, 2, 11, 23)])
        self.assertAlmostEqual(0.658, consumption.buckets[datetime(2025, 2, 12, 0)])
        self.assertAlmostEqual(0.544, consumption.buckets[datetime(2025, 2, 12, 1)])
        self.assertAlmostEqual(1.157, consumption.buckets[datetime(2025, 2, 12, 21)])
        self.assertAlmostEqual(0.641, consumption.buckets[datetime(2025, 2, 12, 22)])
        self.assertAlmostEqual(0.761, consumption.buckets[datetime(2025, 2, 12, 23)])

    def test_errors_if_start_is_not_exact_hour_or_half_hour_time(self) -> None:
        with self.assertRaises(ParserException):
            self.parser.parse(os.path.join(TEST_DATA, "start_is_not_exact_hour_or_half_hour_time.csv"))

    def test_errors_if_end_is_not_exact_hour_or_half_hour_time(self) -> None:
        with self.assertRaises(ParserException):
            self.parser.parse(os.path.join(TEST_DATA, "end_is_not_exact_hour_or_half_hour_time.csv"))

    def test_errors_if_end_is_not_exactly_half_an_hour_after_start(self) -> None:
        with self.assertRaises(ParserException):
            self.parser.parse(os.path.join(TEST_DATA, "end_is_not_exactly_half_an_hour_after_start.csv"))

    def test_errors_if_half_hourly_bucket_is_missing(self) -> None:
        with self.assertRaises(ParserException):
            self.parser.parse(os.path.join(TEST_DATA, "missing_half_hourly_bucket.csv"))
