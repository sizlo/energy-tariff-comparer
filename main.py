import os.path
import sys
import glob

from comparer import Comparer
from config_parser import ConfigParser
from data import Data
from octopus_parser import OctopusParser
from tarrif_parser import TariffParser
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
        print("TODO: write csvs")


if __name__ == "__main__":
    main()
