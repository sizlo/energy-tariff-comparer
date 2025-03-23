from consumption_price import ConsumptionPrice
from consumption import Consumption
from tariff import Tariff


class ConsumptionPriceCalculator:
    def __init__(self, heat_pump_consumption: Consumption, total_consumption: Consumption, tariff: Tariff):
        self.heat_pump_consumption = heat_pump_consumption
        self.total_consumption = total_consumption
        self.tariff = tariff
        self.hourly_prices_without_standing_charge = {}
        self.daily_prices = {}
        self.monthly_prices = {}
        self.yearly_prices = {}
        self.total_price = 0.0

    def calculate_consumption_price(self) -> ConsumptionPrice:
        self.calculate_hourly_prices()
        self.calculate_daily_prices()
        self.calculate_monthly_prices()
        self.calculate_yearly_prices()
        self.calculate_total_price()

        return ConsumptionPrice(
            self.hourly_prices_without_standing_charge,
            self.daily_prices,
            self.monthly_prices,
            self.yearly_prices,
            self.total_price
        )

    def calculate_hourly_prices(self):
        for hour in self.heat_pump_consumption.buckets.keys():
            this_hour_heat_pump_consumption = self.heat_pump_consumption.buckets[hour]
            this_hour_non_heat_pump_consumption = self.total_consumption.buckets[hour] - this_hour_heat_pump_consumption
            price = self.tariff.get_price_in_pence_for_hourly_use(hour, this_hour_heat_pump_consumption,
                                                                  this_hour_non_heat_pump_consumption)
            self.hourly_prices_without_standing_charge[hour] = price

    def calculate_daily_prices(self):
        for hour, hourly_price_without_standing_charge in self.hourly_prices_without_standing_charge.items():
            daily_key = hour.replace(hour=0)
            if daily_key not in self.daily_prices.keys():
                self.daily_prices[daily_key] = self.tariff.daily_standing_charge_pence
            self.daily_prices[daily_key] += hourly_price_without_standing_charge

    def calculate_monthly_prices(self):
        for day, daily_price in self.daily_prices.items():
            monthly_key = day.replace(day=1)
            if monthly_key not in self.monthly_prices.keys():
                self.monthly_prices[monthly_key] = 0.0
            self.monthly_prices[monthly_key] += daily_price

    def calculate_yearly_prices(self):
        for month, monthly_price in self.monthly_prices.items():
            yearly_key = month.replace(month=1)
            if yearly_key not in self.yearly_prices.keys():
                self.yearly_prices[yearly_key] = 0.0
            self.yearly_prices[yearly_key] += monthly_price

    def calculate_total_price(self):
        self.total_price = 0.0
        for yearly_price in self.yearly_prices.values():
            self.total_price += yearly_price

