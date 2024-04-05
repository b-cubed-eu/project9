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
import time
import geopandas as gpd
import rioxarray as rxr
import re

# Parse arguments
parser = argparse.ArgumentParser(
    prog="GBIF-netCDF4 Converter",
    description="Python script to read a GBIF Data Cube and write it to a NetCDF cube.",
    epilog="This script was created at the B-Cubed Hackathon 2024.",
)

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

parser.add_argument(
    "-c",
    "--compression",
    type=bool,
    required=False,
    default=False,
    help="Enable compression for the NetCDF file [default: True]",
)

parser.add_argument(
    "-proj",
    "--projection",
    type=str,
    required=False,
    default="EPSG:3035",
    help="EPSG code for the projection of the NetCDF file [required, default: EPSG:3035]",
)

parser.add_argument(
    "-doi",
    type=str,
    required=False,
    help="Digital Object Identifier (DOI) of the dataset",
)

parser.add_argument(
    "--grid-code-column",
    type=str,
    required=False,
    help="Name of the column containing the EEA grid cell code",
)

# Parse the parameter string on the commandline into the args defined above
ARGS = vars(parser.parse_args())

# Assign the arguments to variables
INPUT_PATH = ARGS["input"]
OUTPUT_PATH = ARGS["output"]
URL = ARGS["url"]
DIMENSIONS = ARGS["dimensions"]
COMPRESSION = ARGS["compression"]
PROJECTION = ARGS["projection"]
DOI = ARGS["doi"]
GRID_CODE_COLUMN = ARGS["grid_code_column"]

try:

    def extract_east_north(text, east_or_north):
        """
        Extracts the easting and northing values from a grid cell code, applying
        a scaling factor based on whether the resolution is in kilometers or meters.

        Parameters:
        text (str): The grid cell code, e.g., '250mE1025N22000'.

        Returns:
        tuple: A tuple containing the scaled easting and northing values, or None if extraction fails.
        """
        # Determine the resolution unit and set the scaling factor
        resolution_match = re.match(r"(\d+)(km|m)", text)
        if resolution_match:
            unit = resolution_match.group(2)
            if unit == "km":
                scaling_factor = 1000
            elif unit == "m":
                scaling_factor = 10
            elif unit is None:
                return None

        else:
            return None  # If the resolution unit is not found

        # Extract the numerical parts of the code
        numbers = re.findall(r"\d+", text)
        if len(numbers) >= 3:  # Ensure there are enough parts in the code
            easting = (
                int(numbers[1]) * scaling_factor
            )  # Apply scaling to the easting value
            northing = (
                int(numbers[2]) * scaling_factor
            )  # Apply scaling to the northing value
            if east_or_north == "east":
                return easting 
            if east_or_north == "north":
                return northing
        else:
            return None

    # Check if the input file was not provided and the URL was
    if INPUT_PATH is None and ARGS["url"] is not None:
        print("Downloading GBIF Data Cube from", ARGS["url"])
        # Download the GBIF Data Cube
        wget.download(ARGS["url"], "data.zip")

        # Extract the zip file
        with zipfile.ZipFile("data.zip", "r") as zip_ref:
            zip_ref.extractall("data")

        # Get paths of files inside the data folder
        files = os.listdir("data")

        # Read the GBIF Data Cube
        df = pd.read_csv(
            f"data/{files[0]}", encoding="utf-8", sep="\t", index_col=False
        )

        # Create Easting and Northing columns from the GRID_CODE_COLUMN
        if GRID_CODE_COLUMN is not None:
            df["easting"] = df[GRID_CODE_COLUMN].apply(
                lambda x: extract_east_north(x, east_or_north= "east")
            )
            df["northing"] = df[GRID_CODE_COLUMN].apply(
                lambda x: extract_east_north(x, east_or_north= "north")
            )
            print("\nEasting and Northing columns created")


        # Infer better dtypes for object columns
        dfn = df.infer_objects()

        # Write the GBIF Data Cube to a NetCDF file
        ds = xr.Dataset.from_dataframe(dfn)

        # Add dimensions to ds from the DIMENSIONS variable
        if DIMENSIONS is not None:
            dimensions = DIMENSIONS.split(",")

            for dimension in dimensions:
                # TODO: strip method is not working
                str_var = str(dimension)
                var = str_var.strip()
                print("\nAdding dimension", var)
                ds = ds.assign_coords({dimension: df[var]})
                if GRID_CODE_COLUMN is not None:
                    ds = ds.assign_coords(
                        {"easting": df["easting"], "northing": df["northing"]}
                    )
                ds.drop_indexes("index", errors="raise")

        # Add attributes to the NetCDF file
        ds.attrs["title"] = "GBIF Data Cube"
        ds.attrs["authors"] = ["Paul Holzschuh", "Luis Maecker", "Taimur Khan"]
        ds.attrs["created_on"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        ds.attrs["source"] = URL or INPUT_PATH
        ds.attrs["history"] = "Created using code from the B-Cubed Hackathon 2024"
        if DOI is not None:
            print("\nAdding DOI", DOI)
            ds.attrs["doi"] = DOI

        # Add the projection to the NetCDF file
        print("\nAdding projection", PROJECTION)
        ds.rio.write_crs(PROJECTION, inplace=True)
        ds.rio.write_grid_mapping(inplace=True)

        # Write the NetCDF file
        # Add compression to the NetCDF file
        if ARGS["compression"]:
            print("\nAdding compression to the NetCDF file")
            comp = dict(compression="zlib", complevel=5)
            encode = {var: comp for var in ds.data_vars}
            ds.to_netcdf(OUTPUT_PATH, encoding=encode)
        else:
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

        # Create Easting and Northing columns from the GRID_CODE_COLUMN
        if GRID_CODE_COLUMN is not None:
            df["easting"] = df[GRID_CODE_COLUMN].apply(
                lambda x: extract_east_north(x, east_or_north= "east")
            )
            df["northing"] = df[GRID_CODE_COLUMN].apply(
                lambda x: extract_east_north(x, east_or_north= "north")
            )
            print("\nEasting and Northing columns created")
            

        # Infer better dtypes for object columns
        dfn = df.infer_objects()

        # Write the GBIF Data Cube to a NetCDF file
        ds = xr.Dataset.from_dataframe(dfn)

        # Add dimensions to ds from the DIMENSIONS variable
        if DIMENSIONS is not None:
            dimensions = DIMENSIONS.split(",")

            for dimension in dimensions:
                # TODO: strip method is not working
                str_var = str(dimension)
                var = str_var.strip()
                print("\nAdding dimension", var)
                ds = ds.assign_coords({dimension: df[var]})
                if GRID_CODE_COLUMN is not None:
                    ds = ds.assign_coords(
                        {"easting": df["easting"], "northing": df["northing"]}
                    )
                # TODO: drop_indexes method is not working
                # ds.drop_indexes("index", errors="raise")

        # Add attributes to the NetCDF file
        ds.attrs["title"] = "GBIF Data Cube"
        ds.attrs["authors"] = ["Paul Holzschuh", "Luis Maecker", "Taimur Khan"]
        ds.attrs["created_on"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        ds.attrs["source"] = URL or INPUT_PATH
        ds.attrs["history"] = "Created using code from the B-Cubed Hackathon 2024"
        if DOI is not None:
            print("\nAdding DOI", DOI)
            ds.attrs["doi"] = DOI

        # Add the projection to the NetCDF file
        print("\nAdding projection", PROJECTION)
        ds.rio.write_crs(PROJECTION, inplace=True)
        ds.rio.write_grid_mapping(inplace=True)

        # Write the NetCDF file
        # Add compression to the NetCDF file
        if ARGS["compression"]:
            print("\nAdding compression to the NetCDF file")
            comp = dict(compression="zlib", complevel=5)
            encode = {var: comp for var in ds.data_vars}
            ds.to_netcdf(OUTPUT_PATH, encoding=encode)

        else:
            ds.to_netcdf(OUTPUT_PATH)
        ds.to_netcdf(OUTPUT_PATH, encoding=encode)

        print("\nNetCDF file written to", OUTPUT_PATH)

except:
    print("An error occurred while processing the data")
    print("Please check the input data and try again")
    os.remove("data.zip")
    shutil.rmtree("data")
    os.remove(OUTPUT_PATH)
    print("Exiting the program")
    exit(1)
