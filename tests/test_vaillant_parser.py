import unittest
import os
from datetime import datetime

from data import Data
from exception import ParserException
from vaillant_parser import VaillantParser

TEST_DATA = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "vaillant")


class VaillantParserTests(unittest.TestCase):

    def setUp(self) -> None:
        self.data = Data()

    def test_gets_correct_count_of_buckets(self) -> None:
        VaillantParser(os.path.join(TEST_DATA, "valid.csv"), self.data).parse()
        self.assertEqual(48, len(self.data.hourly.buckets))

    def test_dhw_values_are_converted_to_kwh(self) -> None:
        VaillantParser(os.path.join(TEST_DATA, "valid.csv"), self.data).parse()
        self.assertAlmostEqual(0.0, self.data.hourly.at_start(datetime(2025, 2, 11, 0)).consumption_kwh.dhw)
        self.assertAlmostEqual(0.0, self.data.hourly.at_start(datetime(2025, 2, 11, 1)).consumption_kwh.dhw)
        self.assertAlmostEqual(0.0, self.data.hourly.at_start(datetime(2025, 2, 11, 2)).consumption_kwh.dhw)
        self.assertAlmostEqual(0.13541758359771014, self.data.hourly.at_start(datetime(2025, 2, 11, 7)).consumption_kwh.dhw)
        self.assertAlmostEqual(0.7704272454316377, self.data.hourly.at_start(datetime(2025, 2, 11, 8)).consumption_kwh.dhw)
        self.assertAlmostEqual(0.7949248559859318, self.data.hourly.at_start(datetime(2025, 2, 11, 9)).consumption_kwh.dhw)
        self.assertAlmostEqual(0.0, self.data.hourly.at_start(datetime(2025, 2, 11, 22)).consumption_kwh.dhw)
        self.assertAlmostEqual(0.0, self.data.hourly.at_start(datetime(2025, 2, 11, 23)).consumption_kwh.dhw)
        self.assertAlmostEqual(0.0, self.data.hourly.at_start(datetime(2025, 2, 12, 0)).consumption_kwh.dhw)
        self.assertAlmostEqual(0.0, self.data.hourly.at_start(datetime(2025, 2, 12, 1)).consumption_kwh.dhw)
        self.assertAlmostEqual(0.0, self.data.hourly.at_start(datetime(2025, 2, 12, 21)).consumption_kwh.dhw)
        self.assertAlmostEqual(0.0, self.data.hourly.at_start(datetime(2025, 2, 12, 22)).consumption_kwh.dhw)
        self.assertAlmostEqual(0.0, self.data.hourly.at_start(datetime(2025, 2, 12, 23)).consumption_kwh.dhw)

    def test_heating_values_are_converted_to_kwh(self) -> None:
        VaillantParser(os.path.join(TEST_DATA, "valid.csv"), self.data).parse()
        self.assertAlmostEqual(0.5234340052816901, self.data.hourly.at_start(datetime(2025, 2, 11, 0)).consumption_kwh.heating)
        self.assertAlmostEqual(0.6798820884683099, self.data.hourly.at_start(datetime(2025, 2, 11, 1)).consumption_kwh.heating)
        self.assertAlmostEqual(0.5674215042483268, self.data.hourly.at_start(datetime(2025, 2, 11, 2)).consumption_kwh.heating)
        self.assertAlmostEqual(0.7068231757698933, self.data.hourly.at_start(datetime(2025, 2, 11, 7)).consumption_kwh.heating)
        self.assertAlmostEqual(0.34163152215789166, self.data.hourly.at_start(datetime(2025, 2, 11, 8)).consumption_kwh.heating)
        self.assertAlmostEqual(0.6360858296605308, self.data.hourly.at_start(datetime(2025, 2, 11, 9)).consumption_kwh.heating)
        self.assertAlmostEqual(0.4977575153212172, self.data.hourly.at_start(datetime(2025, 2, 11, 22)).consumption_kwh.heating)
        self.assertAlmostEqual(0.4160746555144476, self.data.hourly.at_start(datetime(2025, 2, 11, 23)).consumption_kwh.heating)
        self.assertAlmostEqual(0.4051547657790927, self.data.hourly.at_start(datetime(2025, 2, 12, 0)).consumption_kwh.heating)
        self.assertAlmostEqual(0.50407810269105653, self.data.hourly.at_start(datetime(2025, 2, 12, 1)).consumption_kwh.heating)
        self.assertAlmostEqual(0.5142208331138825, self.data.hourly.at_start(datetime(2025, 2, 12, 21)).consumption_kwh.heating)
        self.assertAlmostEqual(0.38658080963103794, self.data.hourly.at_start(datetime(2025, 2, 12, 22)).consumption_kwh.heating)
        self.assertAlmostEqual(0.32021549619682673, self.data.hourly.at_start(datetime(2025, 2, 12, 23)).consumption_kwh.heating)

    def test_heat_pump_values_are_sum_of_dhw_and_heating_usage_converted_to_kwh(self) -> None:
        VaillantParser(os.path.join(TEST_DATA, "valid.csv"), self.data).parse()
        self.assertAlmostEqual(0.5234340052816901, self.data.hourly.at_start(datetime(2025, 2, 11, 0)).consumption_kwh.heat_pump)
        self.assertAlmostEqual(0.6798820884683099, self.data.hourly.at_start(datetime(2025, 2, 11, 1)).consumption_kwh.heat_pump)
        self.assertAlmostEqual(0.5674215042483268, self.data.hourly.at_start(datetime(2025, 2, 11, 2)).consumption_kwh.heat_pump)
        self.assertAlmostEqual(0.84224075937, self.data.hourly.at_start(datetime(2025, 2, 11, 7)).consumption_kwh.heat_pump)
        self.assertAlmostEqual(1.11205876759, self.data.hourly.at_start(datetime(2025, 2, 11, 8)).consumption_kwh.heat_pump)
        self.assertAlmostEqual(1.43101068565, self.data.hourly.at_start(datetime(2025, 2, 11, 9)).consumption_kwh.heat_pump)
        self.assertAlmostEqual(0.4977575153212172, self.data.hourly.at_start(datetime(2025, 2, 11, 22)).consumption_kwh.heat_pump)
        self.assertAlmostEqual(0.4160746555144476, self.data.hourly.at_start(datetime(2025, 2, 11, 23)).consumption_kwh.heat_pump)
        self.assertAlmostEqual(0.4051547657790927, self.data.hourly.at_start(datetime(2025, 2, 12, 0)).consumption_kwh.heat_pump)
        self.assertAlmostEqual(0.50407810269105653, self.data.hourly.at_start(datetime(2025, 2, 12, 1)).consumption_kwh.heat_pump)
        self.assertAlmostEqual(0.5142208331138825, self.data.hourly.at_start(datetime(2025, 2, 12, 21)).consumption_kwh.heat_pump)
        self.assertAlmostEqual(0.38658080963103794, self.data.hourly.at_start(datetime(2025, 2, 12, 22)).consumption_kwh.heat_pump)
        self.assertAlmostEqual(0.32021549619682673, self.data.hourly.at_start(datetime(2025, 2, 12, 23)).consumption_kwh.heat_pump)

    def test_errors_if_start_is_not_exact_hour_time(self) -> None:
        with self.assertRaises(ParserException):
            VaillantParser(os.path.join(TEST_DATA, "start_is_not_exact_hour_time.csv"), self.data).parse()

    def test_errors_if_end_is_not_exact_hour_time(self) -> None:
        with self.assertRaises(ParserException):
            VaillantParser(os.path.join(TEST_DATA, "end_is_not_exact_hour_time.csv"), self.data).parse()

    def test_errors_if_end_is_not_exactly_one_hour_after_start(self) -> None:
        with self.assertRaises(ParserException):
            VaillantParser(os.path.join(TEST_DATA, "end_is_not_exactly_one_hour_after_start.csv"), self.data).parse()

    def test_errors_if_hourly_bucket_is_missing(self) -> None:
        with self.assertRaises(ParserException):
            VaillantParser(os.path.join(TEST_DATA, "missing_hourly_bucket.csv"), self.data).parse()
