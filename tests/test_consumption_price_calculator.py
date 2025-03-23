import unittest
import os
from datetime import datetime

from consumption_price_calculator import ConsumptionPriceCalculator
from octopus_parser import OctopusParser
from tarrif_parser import TariffParser
from vaillant_parser import VaillantParser

TEST_DATA = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

heat_pump_consumption = VaillantParser().parse(os.path.join(TEST_DATA, "vaillant", "bulk.csv"))
total_consumption = OctopusParser().parse(os.path.join(TEST_DATA, "octopus", "bulk.csv"))
standard_tariff = TariffParser().parse(os.path.join(TEST_DATA, "tariffs", "standard_valid.json"))
hourly_variable_tariff = TariffParser().parse(os.path.join(TEST_DATA, "tariffs", "hourly_variable_valid.json"))
flat_heat_pump_rate_tariff = TariffParser().parse(os.path.join(TEST_DATA, "tariffs", "flat_heat_pump_rate_valid.json"))


class ConsumptionPriceCalculatorTests(unittest.TestCase):
    def test_calculates_correct_prices_on_standard_tariff(self):
        consumption_price = ConsumptionPriceCalculator(heat_pump_consumption, total_consumption, standard_tariff).calculate_consumption_price()

        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 0)], 43.63781)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 1)], 31.187)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 2)], 37.4244)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 3)], 32.79433)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 4)], 37.49637)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 5)], 40.49512)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 6)], 28.21224)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 7)], 42.4623)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 8)], 44.33352)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 9)], 33.60999)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 10)], 33.84989)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 11)], 32.12261)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 12)], 26.34102)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 13)], 32.43448)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 14)], 35.31328)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 15)], 34.90545)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 16)], 36.68071)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 17)], 40.44714)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 18)], 35.2653)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 19)], 42.79816)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 20)], 28.69204)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 21)], 36.39283)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 22)], 42.07846)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 23)], 36.00899)

        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 1)], 894.79149)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 2)], 939.26895)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 3)], 874.44797)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 4)], 937.44571)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 5)], 908.15392)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 6)], 877.06288)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 7)], 921.42039)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 8)], 927.29794)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 9)], 897.93418)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 10)], 896.85463)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 11)], 994.03812)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 12)], 886.89878)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 13)], 911.29661)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 14)], 882.55659)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 15)], 902.03647)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 16)], 954.76649)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 17)], 893.40007)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 18)], 905.68295)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 19)], 915.11102)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 20)], 917.05421)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 21)], 933.72726)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 22)], 894.0478)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 23)], 953.87886)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 24)], 908.48978)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 25)], 887.40257)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 26)], 909.49736)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 27)], 915.59082)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 28)], 915.6388)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 29)], 929.62497)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 30)], 934.25504)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 31)], 922.97974)

        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2022, 11, 1)], 17476.25622, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2022, 12, 1)], 28232.15443, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 1, 1)], 28332.43263, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 2, 1)], 25468.08518, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 3, 1)], 28196.88913, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 4, 1)], 27264.36137, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 5, 1)], 28228.388, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 6, 1)], 27516.28036, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 7, 1)], 28160.20842, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 8, 1)], 28393.87102, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 9, 1)], 27196.06184, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 10, 1)], 28329.21797, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 11, 1)], 27412.21174, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 12, 1)], 28147.0619, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 1, 1)], 28251.68229, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 2, 1)], 26332.76922, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 3, 1)], 28435.78155, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 4, 1)], 27148.32174, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 5, 1)], 28286.49178, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 6, 1)], 27301.83375, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 7, 1)], 28471.02286, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 8, 1)], 28342.65237, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 9, 1)], 27604.68351, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 10, 1)], 28259.575, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 11, 1)], 27333.69247, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 12, 1)], 28385.5225, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2025, 1, 1)], 28224.64556, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2025, 2, 1)], 11935.0671, 3)

        self.assertAlmostEqual(consumption_price.yearly_prices_pence[datetime(2022, 1, 1)], 45708.41065, 3)
        self.assertAlmostEqual(consumption_price.yearly_prices_pence[datetime(2023, 1, 1)], 332645.0696, 3)
        self.assertAlmostEqual(consumption_price.yearly_prices_pence[datetime(2024, 1, 1)], 334154.029, 3)
        self.assertAlmostEqual(consumption_price.yearly_prices_pence[datetime(2025, 1, 1)], 40159.7127, 3)

        self.assertAlmostEqual(consumption_price.total_price_pence, 752667.222, 3)

    def test_calculates_correct_prices_on_flat_heat_pump_rate_tariff(self):
        consumption_price = ConsumptionPriceCalculator(heat_pump_consumption, total_consumption, flat_heat_pump_rate_tariff).calculate_consumption_price()

        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 0)], 43.00091736)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 1)], 29.45892768)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 2)], 37.18017576)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 3)], 31.77171624)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 4)], 37.27162944)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 5)], 38.4673836)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 6)], 26.91336384)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 7)], 41.87349936)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 8)], 43.96060152)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 9)], 32.19104592)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 10)], 33.06312312)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 11)], 31.79893704)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 12)], 24.88990968)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 13)], 31.0094616)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 14)], 34.83278472)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 15)], 33.42927528)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 16)], 36.00068952)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 17)], 38.18018952)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 18)], 35.21903328)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 19)], 41.31748632)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 20)], 27.75240624)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 21)], 34.53482208)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 22)], 40.8506664)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 23)], 34.65242088)

        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 1)], 862.3618783)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 2)], 911.0894659)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 3)], 841.7177304)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 4)], 901.849247 )
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 5)], 877.0659629)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 6)], 836.8468378)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 7)], 888.6642286)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 8)], 901.3473955)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 9)], 868.3788598)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 10)], 867.7219994)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 11)], 961.5305419)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 12)], 856.4652506)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 13)], 882.0770719)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 14)], 849.8036722)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 15)], 870.5979329)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 16)], 926.7190037)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 17)], 853.3800062)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 18)], 873.6992354)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 19)], 878.5780202)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 20)], 887.3828009)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 21)], 899.8146972)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 22)], 865.0689823)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 23)], 919.4524063)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 24)], 880.6379532)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 25)], 854.8763986)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 26)], 884.0095627)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 27)], 880.9486956)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 28)], 880.6937678)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 29)], 897.946727)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 30)], 905.6444086)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 31)], 896.6496626)

        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2022, 11, 1)], 16882.46913, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2022, 12, 1)], 27225.90866, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 1, 1)], 27345.84982, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 2, 1)], 24586.41064, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 3, 1)], 27194.87842, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 4, 1)], 26319.53534, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 5, 1)], 27264.46294, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 6, 1)], 26565.78861, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 7, 1)], 27198.34255, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 8, 1)], 27410.43453, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 9, 1)], 26272.32815, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 10, 1)], 27329.2906, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 11, 1)], 26445.99037, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 12, 1)], 27156.17776, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 1, 1)], 27244.16298, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 2, 1)], 25426.21816, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 3, 1)], 27439.25548, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 4, 1)], 26219.55819, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 5, 1)], 27289.2142, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 6, 1)], 26372.64576, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 7, 1)], 27473.79814, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 8, 1)], 27363.0204, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 9, 1)], 26667.11487, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 10, 1)], 27306.99163, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 11, 1)], 26313.69989, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 12, 1)], 27419.12701, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2025, 1, 1)], 27219.87666, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2025, 2, 1)], 11530.6209, 3)

        self.assertAlmostEqual(consumption_price.yearly_prices_pence[datetime(2022, 1, 1)], 44108.37779, 3)
        self.assertAlmostEqual(consumption_price.yearly_prices_pence[datetime(2023, 1, 1)], 321089.4897, 3)
        self.assertAlmostEqual(consumption_price.yearly_prices_pence[datetime(2024, 1, 1)], 322534.8067, 3)
        self.assertAlmostEqual(consumption_price.yearly_prices_pence[datetime(2025, 1, 1)], 38750.4976, 3)

        self.assertAlmostEqual(consumption_price.total_price_pence, 726483.1718, 3)

    def test_calculates_correct_prices_on_hourly_variable_tariff(self):
        consumption_price = ConsumptionPriceCalculator(heat_pump_consumption, total_consumption, hourly_variable_tariff).calculate_consumption_price()

        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 0)], 48.65825)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 1)], 34.775)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 2)], 41.73)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 3)], 36.56725)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 4)], 20.50656)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 5)], 22.14656)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 6)], 15.42912)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 7)], 47.3475)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 8)], 49.434)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 9)], 37.47675)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 10)], 37.74425)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 11)], 35.81825)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 12)], 29.3715)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 13)], 17.73824)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 14)], 19.31264)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 15)], 19.0896)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 16)], 61.34348)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 17)], 67.64232)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 18)], 58.9764)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 19)], 47.722)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 20)], 31.993)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 21)], 40.57975)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 22)], 23.01248)
        self.assertAlmostEqual(consumption_price.hourly_prices_pence_without_standing_charge[datetime(2022, 12, 2, 23)], 19.69312)

        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 1)], 891.76982)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 2)], 934.1084)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 3)], 863.78773)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 4)], 913.60135)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 5)], 908.28868)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 6)], 871.44766)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 7)], 932.16253)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 8)], 918.96989)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 9)], 893.89678)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 10)], 891.36842)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 11)], 1000.02308)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 12)], 878.03332)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 13)], 897.87827)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 14)], 878.1352)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 15)], 923.27598)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 16)], 945.50616)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 17)], 890.50021)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 18)], 907.46258)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 19)], 913.1374)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 20)], 919.17903)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 21)], 933.15657)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 22)], 907.55393)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 23)], 950.20732)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 24)], 906.73337)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 25)], 887.70963)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 26)], 892.56358)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 27)], 923.52873)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 28)], 928.87613)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 29)], 919.13204)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 30)], 925.73094)
        self.assertAlmostEqual(consumption_price.daily_prices_pence[datetime(2024, 8, 31)], 928.1426)

        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2022, 11, 1)], 17359.69194, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2022, 12, 1)], 28108.506, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 1, 1)], 28197.94453, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 2, 1)], 25386.82466, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 3, 1)], 28016.85227, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 4, 1)], 27101.16757, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 5, 1)], 28164.94661, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 6, 1)], 27475.34768, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 7, 1)], 28094.09388, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 8, 1)], 28372.13025, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 9, 1)], 27048.07985, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 10, 1)], 28296.1764, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 11, 1)], 27256.48605, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2023, 12, 1)], 28032.72424, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 1, 1)], 28149.51575, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 2, 1)], 26329.17755, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 3, 1)], 28396.79663, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 4, 1)], 27125.429, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 5, 1)], 28081.63953, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 6, 1)], 27148.24033, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 7, 1)], 28396.00117, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 8, 1)], 28275.86733, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 9, 1)], 27588.92854, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 10, 1)], 28172.70825, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 11, 1)], 27233.58985, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2024, 12, 1)], 28211.19114, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2025, 1, 1)], 28181.30956, 3)
        self.assertAlmostEqual(consumption_price.monthly_prices_pence[datetime(2025, 2, 1)], 11888.5692, 3)

        self.assertAlmostEqual(consumption_price.yearly_prices_pence[datetime(2022, 1, 1)], 45468.19794, 3)
        self.assertAlmostEqual(consumption_price.yearly_prices_pence[datetime(2023, 1, 1)], 331442.774, 3)
        self.assertAlmostEqual(consumption_price.yearly_prices_pence[datetime(2024, 1, 1)], 333109.0851, 3)
        self.assertAlmostEqual(consumption_price.yearly_prices_pence[datetime(2025, 1, 1)], 40069.8788, 3)

        self.assertAlmostEqual(consumption_price.total_price_pence, 750089.9358, 3)
