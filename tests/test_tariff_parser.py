import unittest
import os

from exception import ParserException
from tariff import StandardTariff, HourlyVariableTariff, FlatHeatPumpRateTariff
from tariff_parser import TariffParser

TEST_DATA = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "tariffs")


class TariffParserTests(unittest.TestCase):
    def setUp(self):
        self.parser = TariffParser()

    def test_errors_on_unknown_type(self):
        with self.assertRaises(ParserException):
            self.parser.parse(os.path.join(TEST_DATA, "unknown_type.json"))

    def test_errors_on_missing_type(self):
        with self.assertRaises(ParserException):
            self.parser.parse(os.path.join(TEST_DATA, "missing_type.json"))

    def test_errors_on_missing_name(self):
        with self.assertRaises(ParserException):
            self.parser.parse(os.path.join(TEST_DATA, "missing_name.json"))

    def test_errors_on_missing_daily_standing_charge(self):
        with self.assertRaises(ParserException):
            self.parser.parse(os.path.join(TEST_DATA, "missing_daily_standing_charge.json"))

    def test_errors_on_standard_missing_unit_rate(self):
        with self.assertRaises(ParserException):
            self.parser.parse(os.path.join(TEST_DATA, "standard_missing_unit_rate.json"))

    def test_parses_standard_tariff(self):
        tariff = self.parser.parse(os.path.join(TEST_DATA, "standard_valid.json"))
        self.assertIsInstance(tariff, StandardTariff)
        self.assertEqual("Valid Standard Test Tariff", tariff.name)
        self.assertEqual(49.12, tariff.daily_standing_charge_pence)
        self.assertEqual(23.99, tariff.unit_price_pence_per_kwh)

    def test_errors_on_hourly_variable_missing_hourly_rates(self):
        with self.assertRaises(ParserException):
            self.parser.parse(os.path.join(TEST_DATA, "hourly_variable_missing_hourly_rates.json"))

    def test_errors_on_hourly_variable_having_incomplete_hourly_rates(self):
        with self.assertRaises(ParserException):
            self.parser.parse(os.path.join(TEST_DATA, "hourly_variable_incomplete_hourly_rates.json"))

    def test_errors_on_hourly_variable_having_extra_int_key_in_hourly_rates(self):
        with self.assertRaises(ParserException):
            self.parser.parse(os.path.join(TEST_DATA, "hourly_variable_extra_int_key_in_hourly_rates.json"))

    def test_errors_on_hourly_variable_having_extra_str_key_in_hourly_rates(self):
        with self.assertRaises(ParserException):
            self.parser.parse(os.path.join(TEST_DATA, "hourly_variable_extra_str_key_in_hourly_rates.json"))

    def test_parses_hourly_variable_tariff(self):
        tariff = self.parser.parse(os.path.join(TEST_DATA, "hourly_variable_valid.json"))
        self.assertIsInstance(tariff, HourlyVariableTariff)
        self.assertEqual("Valid Hourly Variable Test Tariff", tariff.name)
        self.assertEqual(49.98, tariff.daily_standing_charge_pence)
        expected_hourly_rates = {
            0: 26.75,
            1: 26.75,
            2: 26.75,
            3: 26.75,
            4: 13.12,
            5: 13.12,
            6: 13.12,
            7: 26.75,
            8: 26.75,
            9: 26.75,
            10: 26.75,
            11: 26.75,
            12: 26.75,
            13: 13.12,
            14: 13.12,
            15: 13.12,
            16: 40.12,
            17: 40.12,
            18: 40.12,
            19: 26.75,
            20: 26.75,
            21: 26.75,
            22: 13.12,
            23: 13.12
          }
        self.assertEqual(expected_hourly_rates, tariff.hourly_unit_rates_pence_per_kwh)

    def test_errors_on_flat_heat_pump_rate_missing_heat_pump_unit_rate(self):
        with self.assertRaises(ParserException):
            self.parser.parse(os.path.join(TEST_DATA, "flat_heat_pump_rate_missing_heat_pump_unit_rate.json"))

    def test_errors_on_flat_heat_pump_rate_missing_non_heat_pump_unit_rate(self):
        with self.assertRaises(ParserException):
            self.parser.parse(os.path.join(TEST_DATA, "flat_heat_pump_rate_missing_non_heat_pump_unit_rate.json"))

    def test_parses_flat_heat_pump_rate_tariff(self):
        tariff = self.parser.parse(os.path.join(TEST_DATA, "flat_heat_pump_rate_valid.json"))
        self.assertIsInstance(tariff, FlatHeatPumpRateTariff)
        self.assertEqual("Valid Flat Heat Pump Rate Test Tariff", tariff.name)
        self.assertEqual(49.17, tariff.daily_standing_charge_pence)
        self.assertEqual(15.0, tariff.heat_pump_unit_rate_pence_per_kwh)
        self.assertEqual(24.36, tariff.non_heat_pump_unit_rate_pence_per_kwh)
