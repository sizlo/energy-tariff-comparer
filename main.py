import sys

from comparer import Comparer
from config_parser import ConfigParser
from csv_writer import CsvWriter
from data import Data
from octopus_parser import OctopusParser
from tariff_parser import TariffParser
from vaillant_parser import VaillantParser


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <config_file_path>")
        sys.exit(1)

    config = ConfigParser(sys.argv[1]).parse()

    data = Data()

    VaillantParser(config.vaillant_file_path, data).parse()
    OctopusParser(config.octopus_file_path, data).parse()

    tariffs = [TariffParser().parse(file) for file in config.tariff_file_paths]

    Comparer(data, tariffs).compare()

    if config.csv_output_file_path is not None:
        CsvWriter(data, config.csv_output_file_path).write()


if __name__ == "__main__":
    main()
