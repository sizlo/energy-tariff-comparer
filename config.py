from typing import List


class Config:
    def __init__(self, vaillant_file_path: str, octopus_file_path: str, tariff_file_paths: List[str], csv_output_dir_path: str | None):
        self.vaillant_file_path: str = vaillant_file_path
        self.octopus_file_path: str = octopus_file_path
        self.tariff_file_paths: List[str] = tariff_file_paths
        self.csv_output_file_path: str | None = csv_output_dir_path
