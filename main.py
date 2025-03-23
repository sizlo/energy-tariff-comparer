import os.path
import sys
import glob

from comparer import Comparer
from octopus_parser import OctopusParser
from tarrif_parser import TariffParser
from vaillant_parser import VaillantParser


def main():
    data_path = sys.argv[1]

    heat_pump_consumption = VaillantParser().parse(os.path.join(data_path, "usage", "vaillant.csv"))
    total_consumption = OctopusParser().parse(os.path.join(data_path, "usage", "octopus.csv"))
    tariffs = [TariffParser().parse(file) for file in glob.glob(f"{data_path}/tariffs/*.json")]

    Comparer(heat_pump_consumption, total_consumption, tariffs).compare()


if __name__ == "__main__":
    main()
