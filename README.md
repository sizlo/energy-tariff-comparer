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

## Supported tariff types

See the [TariffType enum](tariff.py) for descriptions of the supported tariff types.

## Running

Install dependencies: `pip install -r requirements.txt`

Run: `python3 main.py <config_file_path>`

The config file points the script to the consumption and tariff data files. See [here](data/2025-03-23/config.yaml) for an example.

## View graphs

This repo contains an html/js based graph viewer which works with the csv files outputted by the script. It requires running chrome in a mode that allows javascript to load files from the local disk. To run the graph viewer run the following from the repo root:

`./grapher/open.sh`

Then input the csv file path, choose what prices to compare, and hit render.
