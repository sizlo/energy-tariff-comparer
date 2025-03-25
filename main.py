import os.path
import sys
import glob

from comparer import Comparer
from data import Data
from octopus_parser import OctopusParser
from tarrif_parser import TariffParser
from vaillant_parser import VaillantParser


def main():
    data_path = sys.argv[1]

    data = Data()

    VaillantParser(os.path.join(data_path, "usage", "vaillant.csv"), data).parse()
    OctopusParser(os.path.join(data_path, "usage", "octopus.csv"), data).parse()

    tariffs = [TariffParser().parse(file) for file in glob.glob(f"{data_path}/tariffs/*.json")]

    Comparer(data, tariffs).compare()

    # TODO - write data to csvs, controllable by CLI


if __name__ == "__main__":
    main()
