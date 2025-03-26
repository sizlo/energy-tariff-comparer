energy-tariff-comparer
======================

Script to compare the prices charged by different energy tariffs based on real energy consumption data. Only supports electrical consumption.

The script can be configured to output the consumption and price data to CSVs bucketed by hour, day, month, year, and the entire period processed.

The goal is to find the cheapest tariff to run my heat pump system on.

## Supported energy consumption data sources:

All consumption data is parsed from CSV files. Currently supported sources for these CSV files are:

#### Octopus energy

Can be downloaded from your account in the Octopus website. The data is bucketed by half hours, this script turns them into full hour buckets as it parses the csv.

#### vaillant-poller

Another project written by me which polls the Vaillant API and dumps consumption data to CSV files. [Link to project](https://github.com/sizlo/vaillant-poller).

## Running

Install dependencies: `pip install -r requirements.txt`

Run: `python3 main.py <config_file_path>`

The config file points the script to the consumption and tariff data files. See [here](data/2025-03-23/config.yaml) for an example.
