import unittest
import os
from datetime import datetime

from data import Data
from exception import ParserException
from octopus_parser import OctopusParser

TEST_DATA = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "octopus")


class OctopusParserTests(unittest.TestCase):

    def setUp(self) -> None:
        self.data = Data()

    def test_gets_correct_count_of_buckets(self) -> None:
        OctopusParser(os.path.join(TEST_DATA, "valid.csv"), self.data).parse()
        self.assertEqual(48, len(self.data.hourly.buckets))

    def test_bucket_values_are_sum_of_each_half_hour_within_hour(self) -> None:
        OctopusParser(os.path.join(TEST_DATA, "valid.csv"), self.data).parse()
        self.assertAlmostEqual(0.691, self.data.hourly.at_start(datetime(2025, 2, 11, 0)).consumption_kwh.total)
        self.assertAlmostEqual(0.829, self.data.hourly.at_start(datetime(2025, 2, 11, 1)).consumption_kwh.total)
        self.assertAlmostEqual(0.665, self.data.hourly.at_start(datetime(2025, 2, 11, 2)).consumption_kwh.total)
        self.assertAlmostEqual(0.457, self.data.hourly.at_start(datetime(2025, 2, 11, 22)).consumption_kwh.total)
        self.assertAlmostEqual(0.752, self.data.hourly.at_start(datetime(2025, 2, 11, 23)).consumption_kwh.total)
        self.assertAlmostEqual(0.658, self.data.hourly.at_start(datetime(2025, 2, 12, 0)).consumption_kwh.total)
        self.assertAlmostEqual(0.544, self.data.hourly.at_start(datetime(2025, 2, 12, 1)).consumption_kwh.total)
        self.assertAlmostEqual(1.157, self.data.hourly.at_start(datetime(2025, 2, 12, 21)).consumption_kwh.total)
        self.assertAlmostEqual(0.641, self.data.hourly.at_start(datetime(2025, 2, 12, 22)).consumption_kwh.total)
        self.assertAlmostEqual(0.761, self.data.hourly.at_start(datetime(2025, 2, 12, 23)).consumption_kwh.total)

    def test_errors_if_start_is_not_exact_hour_or_half_hour_time(self) -> None:
        with self.assertRaises(ParserException):
            OctopusParser(os.path.join(TEST_DATA, "start_is_not_exact_hour_or_half_hour_time.csv"), self.data).parse()

    def test_errors_if_end_is_not_exact_hour_or_half_hour_time(self) -> None:
        with self.assertRaises(ParserException):
            OctopusParser(os.path.join(TEST_DATA, "end_is_not_exact_hour_or_half_hour_time.csv"), self.data).parse()

    def test_errors_if_end_is_not_exactly_half_an_hour_after_start(self) -> None:
        with self.assertRaises(ParserException):
            OctopusParser(os.path.join(TEST_DATA, "end_is_not_exactly_half_an_hour_after_start.csv"), self.data).parse()

    def test_errors_if_half_hourly_bucket_is_missing(self) -> None:
        with self.assertRaises(ParserException):
            OctopusParser(os.path.join(TEST_DATA, "missing_half_hourly_bucket.csv"), self.data).parse()
