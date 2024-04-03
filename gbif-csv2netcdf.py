#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename          : netcdf.py
# description       : Python script to read a GBIF Data Cube (as local CSV or remote URL) and write it to a NetCDF file
# author            : Paul Holzschuh, Luis Maecker, Taimur Khan
# email             : taimur.khan@ufz.de, luis_maecker@web.de, paul.holzschuh@gmail.com
# date              : 2024-03-01
# version           : 1
# usage             : python3 -m venv path/to/venv && source path/to/venv/bin/activate && pip install -r requirements.txt && python gbif-csv2netcdf.py -h
# notes             : Sample dataset: #https://api.gbif.org/v1/occurrence/download/request/0000025-240314170635999.zip"
# license           : MIT
# py version        : 3.11.7
# ==============================================================================



# Import required libraries
import xarray as xr
import numpy as np
import pandas as pd
import os
import argparse
import wget
import zipfile
import shutil

# Parse arguments
parser = argparse.ArgumentParser(
    prog="GBIF-netCDF4 Converter",
    description="Python script to read a GBIF Data Cube and write it to a NetCDF cube.",
    epilog="This script was created at the B-Cubed Hackathon 2024.",
)

# TODO
parser.add_argument(
    "-i", "--input", type=str, required=False, help="Path to local input CSV file"
)

parser.add_argument(
    "-u", "--url", type=str, required=False, help="URL to GBIF Data Cube"
)

parser.add_argument(
    "-dims",
    "--dimensions",
    type=str,
    required=False,
    help="Comma seperated list of dimensions in netCDF4 cube",
)

parser.add_argument(
    "-o",
    "--output",
    type=str,
    required=True,
    help="Path to output NetCDF file [required]",
)


# Parse the parameter string on the commandline into the args defined above
ARGS = vars(parser.parse_args())

# Assign the arguments to variables
INPUT_PATH = ARGS["input"]
OUTPUT_PATH = ARGS["output"]
URL = ARGS["url"]
DIMENSIONS = ARGS["dimensions"]

# Check if the input file was not provided and the URL was
if INPUT_PATH is None and ARGS["url"] is not None:
    print("Downloading GBIF Data Cube from", ARGS["url"])
    # Download the GBIF Data Cube
    wget.download(ARGS["url"], "data.zip")
    
    # Extract the zip file
    with zipfile.ZipFile("data.zip", 'r') as zip_ref:
        zip_ref.extractall("data")
        
    # Get paths of files inside the data folder
    files = os.listdir("data") 

    # Read the GBIF Data Cube
    df = pd.read_csv(f"data/{files[0]}", encoding="utf-8", sep="\t", index_col=False)

    # Write the GBIF Data Cube to a NetCDF file
    ds = xr.Dataset.from_dataframe(df)

    # Add dimensions to ds from the DIMENSIONS variable
    if DIMENSIONS is not None:
        dimensions = DIMENSIONS.split(",")

        for dimension in dimensions:
            # TODO: strip method is not working
            str_var = str(dimension)
            var = str_var.strip()
            print("\nAdding dimension", var)
            ds = ds.assign_coords({dimension: df[var]})
            ds.drop_indexes("index", errors="raise")
            
    # Write the NetCDF file
    ds.to_netcdf(OUTPUT_PATH)

    print("\nNetCDF file written to", OUTPUT_PATH)
    
    # Remove the zip file and the data folder
    os.remove("data.zip")
    shutil.rmtree("data") 


# If the input file was provided, read the file
else:
    print("\nReading GBIF Data Cube from", INPUT_PATH)

    # Read the GBIF Data Cube
    df = pd.read_csv(INPUT_PATH, encoding="utf-8", sep="\t", index_col=False)

    # Write the GBIF Data Cube to a NetCDF file
    ds = xr.Dataset.from_dataframe(df)

    # Add dimensions to ds from the DIMENSIONS variable
    if DIMENSIONS is not None:
        dimensions = DIMENSIONS.split(",")

        for dimension in dimensions:
            # TODO: strip method is not working
            str_var = str(dimension)
            var = str_var.strip()
            print("\nAdding dimension", var)
            ds = ds.assign_coords({dimension: df[var]})
            # TODO: drop_indexes method is not working
            #ds.drop_indexes("index", errors="raise")

    ds.to_netcdf(OUTPUT_PATH)

    print("\nNetCDF file written to", OUTPUT_PATH)
