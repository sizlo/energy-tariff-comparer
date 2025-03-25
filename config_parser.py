import os.path

import yaml

from config import Config


class ConfigParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self) -> Config:
        config_dir = os.path.dirname(self.file_path)

        with open(self.file_path) as file:
            yaml_data = yaml.safe_load(file)

            csv_output_dir = None
            if "csvOutputDir" in yaml_data.keys():
                csv_output_dir = f"{config_dir}/{yaml_data['csvOutputDir']}"

            return Config(
                f"{config_dir}/{yaml_data['vaillantData']}",
                f"{config_dir}/{yaml_data['octopusData']}",
                [f"{config_dir}/{tariff_file}" for tariff_file in yaml_data['tariffData']],
                csv_output_dir
            )

