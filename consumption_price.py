from datetime import datetime
from typing import Dict


class ConsumptionPrice:
    def __init__(
            self,
            hourly_prices_pence_without_standing_charge: Dict[datetime, float],
            daily_prices_pence: Dict[datetime, float],
            monthly_prices_pence: Dict[datetime, float],
            yearly_prices_pence: Dict[datetime, float],
            total_price_pence: float
    ):
        self.hourly_prices_pence_without_standing_charge = hourly_prices_pence_without_standing_charge
        self.daily_prices_pence = daily_prices_pence
        self.monthly_prices_pence = monthly_prices_pence
        self.yearly_prices_pence = yearly_prices_pence
        self.total_price_pence = total_price_pence
