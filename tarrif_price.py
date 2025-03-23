from consumption_price import ConsumptionPrice
from tariff import Tariff


class TariffPrice:
    def __init__(self, tariff: Tariff, consumption_price: ConsumptionPrice):
        self.tariff = tariff
        self.consumption_price = consumption_price
