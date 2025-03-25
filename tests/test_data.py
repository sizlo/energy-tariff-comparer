import unittest
from datetime import datetime

from data import Data


class DataTests(unittest.TestCase):
    def setUp(self):
        self.dhw_consumption = 1
        self.heating_consumption = 2
        self.total_consumption = 7

        self.hour = datetime(2025, 3, 12, 6)
        self.data = Data()

    def test_calculates_combined_heat_pump_consumption(self):
        self.data.hourly.set_heat_pump_consumption(self.hour, self.dhw_consumption, self.heating_consumption)
        self.assertEqual(3, self.data.hourly.at_start(self.hour).consumption_kwh.heat_pump)

    def test_does_not_populate_non_heat_pump_consumption_when_only_heat_pump_consumption_is_set(self):
        self.data.hourly.set_heat_pump_consumption(self.hour, self.dhw_consumption, self.heating_consumption)
        self.assertIsNone(self.data.hourly.at_start(self.hour).consumption_kwh.non_heat_pump)

    def test_does_not_populate_non_heat_pump_consumption_when_only_total_consumption_is_set(self):
        self.data.hourly.set_total_consumption(self.hour, self.heating_consumption)
        self.assertIsNone(self.data.hourly.at_start(self.hour).consumption_kwh.non_heat_pump)

    def test_updates_non_heat_pump_consumption_when_setting_total_consumption(self):
        self.data.hourly.set_heat_pump_consumption(self.hour, self.dhw_consumption, self.heating_consumption)
        self.data.hourly.set_total_consumption(self.hour, self.total_consumption)
        self.assertEqual(4, self.data.hourly.at_start(self.hour).consumption_kwh.non_heat_pump)

    def test_updates_non_heat_pump_consumption_when_setting_heat_pump_consumption(self):
        self.data.hourly.set_heat_pump_consumption(self.hour, self.dhw_consumption, self.heating_consumption)
        self.data.hourly.set_total_consumption(self.hour, self.total_consumption)
        self.assertEqual(4, self.data.hourly.at_start(self.hour).consumption_kwh.non_heat_pump)
