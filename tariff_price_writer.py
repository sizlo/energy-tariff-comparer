import csv
import os.path
from datetime import datetime
from typing import Callable, Dict, List

from tarrif_price import TariffPrice
from util import render_price


class TariffPriceWriter:
    def __init__(self, tariff_prices: List[TariffPrice], file_path: str):
        self.tariff_prices = tariff_prices
        self.file_path = file_path

    def write(self):
        print("**** Writing csvs ****")
        self.write_hourly_prices()
        self.write_daily_prices()
        self.write_monthly_prices()
        self.write_yearly_prices()
        self.write_total_prices()
        print()

    def write_hourly_prices(self):
        self.write_date_price_dict(
            "hourly_prices_without_standing_charge.csv",
            lambda tp: tp.consumption_price.hourly_prices_pence_without_standing_charge
        )

    def write_daily_prices(self):
        self.write_date_price_dict(
            "daily_prices.csv",
            lambda tp: tp.consumption_price.daily_prices_pence
        )

    def write_monthly_prices(self):
        self.write_date_price_dict(
            "monthly_prices.csv",
            lambda tp: tp.consumption_price.monthly_prices_pence
        )

    def write_yearly_prices(self):
        self.write_date_price_dict(
            "yearly_prices.csv",
            lambda tp: tp.consumption_price.yearly_prices_pence
        )

    def write_total_prices(self):
        full_path = os.path.join(self.file_path, "total_prices.csv")
        with open(full_path, "w") as file:
            writer = csv.writer(file)
            writer.writerow([tp.tariff.name for tp in self.tariff_prices])
            writer.writerow([render_price(tp.consumption_price.total_price_pence) for tp in self.tariff_prices])
            print(f"Written {full_path}")

    def write_date_price_dict(
            self,
            file_name: str,
            get_prices: Callable[[TariffPrice], Dict[datetime, float]],
    ):
        full_path = os.path.join(self.file_path, file_name)
        with open(full_path, "w") as file:
            buckets = list(get_prices(self.tariff_prices[0]).keys())

            writer = csv.writer(file)

            columns = ["ChargePeriodStart"]
            for tariff_price in self.tariff_prices:
                columns.append(tariff_price.tariff.name)
            writer.writerow(columns)

            for bucket in buckets:
                row = [bucket.isoformat()]
                for tariff_price in self.tariff_prices:
                    row.append(render_price(get_prices(tariff_price)[bucket]))
                writer.writerow(row)

        print(f"Written {full_path}")
