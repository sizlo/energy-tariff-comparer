import csv
import errno
import os

from dateutil.relativedelta import relativedelta

from data import Data, TimeBucketedData, BucketData


class CsvWriter:
    def __init__(self, data: Data, output_dir_path: str):
        self.data = data
        self.output_dir_path = output_dir_path
        self.ordered_tariff_names = [
            tariff_price.tariff.name for tariff_price in
            sorted(self.data.total.tariff_prices_pence.values(), key=lambda tariff_price: tariff_price.total)
        ]

    def write(self):
        print("**** Writing csvs ****")
        self.ensure_dirs_exists()
        self.write_time_bucketed_data(self.data.hourly, f"{self.output_dir_path}/hourly.csv")
        self.write_time_bucketed_data(self.data.daily, f"{self.output_dir_path}/daily.csv")
        self.write_time_bucketed_data(self.data.monthly, f"{self.output_dir_path}/monthly.csv")
        self.write_time_bucketed_data(self.data.yearly, f"{self.output_dir_path}/yearly.csv")
        self.write_total_data()
        print()

    def write_time_bucketed_data(self, time_bucketed_data: TimeBucketedData, file_path: str):
        is_hourly = time_bucketed_data.timespan == relativedelta(hours=1)
        with open(file_path, "w") as file:
            writer = csv.writer(file)
            self.write_headers(writer, is_hourly)
            for bucket in time_bucketed_data.buckets.values():
                self.write_bucket(writer, bucket, is_hourly)
        print(f"Written file {file_path}")

    def write_total_data(self):
        file_path = f"{self.output_dir_path}/total.csv"
        with open(file_path, "w") as file:
            writer = csv.writer(file)
            self.write_headers(writer, False)
            self.write_bucket(writer, self.data.total, False)
        print(f"Written file {file_path}")

    def write_headers(self, writer, is_hourly: bool):
        headers = [
            "Start",
            "End",
            "Heat pump dhw consumption (kwh)",
            "Heat pump heating consumption (kwh)",
            "Total heat pump consumption (kwh)",
            "Non heat pump consumption (kwh)",
            "Total overall consumption (kwh)",
        ]

        for tariff_name in self.ordered_tariff_names:
            headers.append(f"{tariff_name} --- Heat pump dhw price (GBP)")
            headers.append(f"{tariff_name} --- Heat pump heating price (GBP)")
            headers.append(f"{tariff_name} --- Total heat pump price (GBP)")
            headers.append(f"{tariff_name} --- Non heat pump price (GBP)")
            if is_hourly:
                headers.append(f"{tariff_name} --- Total price ignoring standing charge (GBP)")
            else:
                headers.append(f"{tariff_name} --- Standing charge price (GBP)")
                headers.append(f"{tariff_name} --- Total price (GBP)")

        writer.writerow(headers)

    def write_bucket(self, writer, bucket: BucketData, is_hourly: bool):
        row = [
            bucket.start,
            bucket.end,
            bucket.consumption_kwh.dhw,
            bucket.consumption_kwh.heating,
            bucket.consumption_kwh.heat_pump,
            bucket.consumption_kwh.non_heat_pump,
            bucket.consumption_kwh.total,
        ]

        for tariff_name in self.ordered_tariff_names:
            row.append(self.render_price(bucket.tariff_prices_pence[tariff_name].dhw))
            row.append(self.render_price(bucket.tariff_prices_pence[tariff_name].heating))
            row.append(self.render_price(bucket.tariff_prices_pence[tariff_name].heat_pump))
            row.append(self.render_price(bucket.tariff_prices_pence[tariff_name].non_heat_pump))
            if is_hourly:
                row.append(self.render_price(bucket.tariff_prices_pence[tariff_name].total))
            else:
                row.append(self.render_price(bucket.tariff_prices_pence[tariff_name].standing_charge))
                row.append(self.render_price(bucket.tariff_prices_pence[tariff_name].total))

        writer.writerow(row)

    def ensure_dirs_exists(self):
        try:
            os.makedirs(os.path.dirname(self.output_dir_path))
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    @staticmethod
    def render_price(price_in_pence: float) -> str:
        price_in_pounds = price_in_pence / 100
        return f"{price_in_pounds:.2f}"
