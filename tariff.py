from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Dict


class TariffType(Enum):
    STANDARD = "STANDARD"
    HOURLY_VARIABLE = "HOURLY_VARIABLE"
    FLAT_HEAT_PUMP_RATE = "FLAT_HEAT_PUMP_RATE"


class Tariff(ABC):
    def __init__(self, name: str, daily_standing_charge_pence):
        self.name = name
        self.daily_standing_charge_pence = daily_standing_charge_pence

    @abstractmethod
    def get_price_in_pence_for_hourly_heat_pump_use(self, hour_start: datetime, usage_kwh: float) -> float:
        pass

    @abstractmethod
    def get_price_in_pence_for_hourly_non_heat_pump_use(self, hour_start: datetime, usage_kwh: float) -> float:
        pass


class StandardTariff(Tariff):
    def __init__(self, name: str, daily_standing_charge_pence: float, unit_price_pence_per_kwh: float):
        super().__init__(name, daily_standing_charge_pence)
        self.unit_price_pence_per_kwh = unit_price_pence_per_kwh

    def get_price_in_pence_for_hourly_heat_pump_use(self, hour_start: datetime, usage_kwh: float) -> float:
        return usage_kwh * self.unit_price_pence_per_kwh

    def get_price_in_pence_for_hourly_non_heat_pump_use(self, hour_start: datetime, usage_kwh: float) -> float:
        return usage_kwh * self.unit_price_pence_per_kwh


class HourlyVariableTariff(Tariff):
    def __init__(self, name: str, daily_standing_charge_pence: float, hourly_unit_rates_pence_per_kwh: Dict[int, float]):
        super().__init__(name, daily_standing_charge_pence)
        self.hourly_unit_rates_pence_per_kwh = hourly_unit_rates_pence_per_kwh

    def get_price_in_pence_for_hourly_heat_pump_use(self, hour_start: datetime, usage_kwh: float) -> float:
        return usage_kwh * self.hourly_unit_rates_pence_per_kwh[hour_start.hour]

    def get_price_in_pence_for_hourly_non_heat_pump_use(self, hour_start: datetime, usage_kwh: float) -> float:
        return usage_kwh * self.hourly_unit_rates_pence_per_kwh[hour_start.hour]


class FlatHeatPumpRateTariff(Tariff):
    def __init__(self, name: str, daily_standing_charge_pence: float, heat_pump_unit_rate_pence_per_kwh: float, non_heat_pump_unit_rate_pence_per_kwh: float):
        super().__init__(name, daily_standing_charge_pence)
        self.heat_pump_unit_rate_pence_per_kwh = heat_pump_unit_rate_pence_per_kwh
        self.non_heat_pump_unit_rate_pence_per_kwh = non_heat_pump_unit_rate_pence_per_kwh

    def get_price_in_pence_for_hourly_heat_pump_use(self, hour_start: datetime, usage_kwh: float) -> float:
        return usage_kwh * self.heat_pump_unit_rate_pence_per_kwh

    def get_price_in_pence_for_hourly_non_heat_pump_use(self, hour_start: datetime, usage_kwh: float) -> float:
        return usage_kwh * self.non_heat_pump_unit_rate_pence_per_kwh
