import json
from typing import Dict, Any

from exception import ParserException
from tariff import Tariff, TariffType, StandardTariff, HourlyVariableTariff, FlatHeatPumpRateTariff


class TariffParser:
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.file_path = ""
        self.name = ""
        self.standing_charge = 0.0

    def parse(self, file_path: str) -> Tariff:
        self.file_path = file_path
        with open(self.file_path) as file:
            self.data = json.load(file)

        self.validate_keys_exist("type", "name", "daily_standing_charge_pence")
        self.name = self.data["name"]
        self.standing_charge = float(self.data["daily_standing_charge_pence"])

        if self.data["type"] == TariffType.STANDARD.value:
            return self.parse_standard()
        elif self.data["type"] == TariffType.HOURLY_VARIABLE.value:
            return self.parse_hourly_variable()
        elif self.data["type"] == TariffType.FLAT_HEAT_PUMP_RATE.value:
            return self.parse_flat_heat_pump_rate()

        raise ParserException(f"Unknown tariff type '{self.data['type']}' from file_path={self.file_path}")

    def parse_standard(self) -> Tariff:
        self.validate_keys_exist("unit_rate_pence_per_kwh")
        unit_rate = float(self.data["unit_rate_pence_per_kwh"])
        return StandardTariff(self.name, self.standing_charge, unit_rate)

    def parse_hourly_variable(self) -> Tariff:
        self.validate_keys_exist("hourly_unit_rates_pence_per_kwh")
        raw_hourly_rates = self.data["hourly_unit_rates_pence_per_kwh"]

        for hour in range(0, 24):
            if str(hour) not in raw_hourly_rates.keys():
                raise ParserException(f"Tariff json is missing unit rate for hour={hour}, file_path={self.file_path}")

        for key in raw_hourly_rates.keys():
            if key not in [str(hour) for hour in range(0, 24)]:
                raise ParserException(f"Tariff json contains unexpected key in hourly rate map key={key}, file_path={self.file_path}")

        hourly_rates = {int(key): value for key, value in raw_hourly_rates.items()}

        return HourlyVariableTariff(self.name, self.standing_charge, hourly_rates)

    def parse_flat_heat_pump_rate(self) -> Tariff:
        self.validate_keys_exist("heat_pump_unit_rate_pence_per_kwh")
        self.validate_keys_exist("non_heat_pump_unit_rate_pence_per_kwh")
        heat_pump_unit_rate_pence_per_kwh = float(self.data["heat_pump_unit_rate_pence_per_kwh"])
        non_heat_pump_unit_rate_pence_per_kwh = float(self.data["non_heat_pump_unit_rate_pence_per_kwh"])
        return FlatHeatPumpRateTariff(self.name, self.standing_charge, heat_pump_unit_rate_pence_per_kwh, non_heat_pump_unit_rate_pence_per_kwh)

    def validate_keys_exist(self, *keys: str):
        for key in keys:
            if key not in self.data.keys():
                raise ParserException(f"Tariff json is missing '{key}' key, file_path={self.file_path}")


