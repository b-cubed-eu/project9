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

# to import to geotiff and geojson
# import rasterio
import rioxarray
# import geojson

#to extract coordinates
import re

# wget and rioxarray were possible to install only through "pip..." in conda environment through anaconda prompt.
# another way ("conda install -c conda-forge") faced issues

# not clear if rasterio should be imported or rioxarray will import it automatically

# Parse arguments
parser = argparse.ArgumentParser(
    prog="GBIF-Geotiff Converter",
    description="Python script to read a GBIF Data Cube and write it to a Geotiff multi-band file.",
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
    help="Comma separated list of bands in Geotiff (or dimensions in GBIF datacube)",
)

parser.add_argument(
    "-o",
    "--output",
    type=str,
    required=True,
    help="Path to the output Geotiff file [required]",
)

# Parse the parameter string on the commandline into the args defined above
ARGS = vars(parser.parse_args())

# Assign the arguments to variables
INPUT_PATH = ARGS["input"]
OUTPUT_PATH = ARGS["output"]
URL = ARGS["url"]
DIMENSIONS = ARGS["dimensions"]

# Extraxt the EAST coordinate
def extract_east_number(text):
    numbers = re.findall(r'\d+', text)
    if len(numbers) >= 2:
        return int(numbers[1])  # Extract the second number
    else:
        return None

# Extraxt the NORTH coordinate
def extract_north_number(text):
    numbers = re.findall(r'\d+', text)
    if len(numbers) >= 2:
        return int(numbers[2])  # Extract the second number
    else:
        return None

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

    # Apply the function to the text_column and create a new column
    df['east_number'] = df['eeacellcode'].apply(lambda x: extract_east_number(x))
    df['north_number'] = df['eeacellcode'].apply(lambda x: extract_north_number(x))

    ## get final coordinate: - for 1000m reslolution:
    df['east_coord_epsg3035_m'] = df['east_number'] * 1000
    df['north_coord_epsg3035_m'] = df['north_number'] * 1000

    # Write the GBIF Data Cube to a Geotiff file
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
            print("Dimensions in the dataset:", ds.dims)

    # Add attributes to the Geotiff file
    ds.attrs["title"] = "GBIF Data Cube"
    ds.attrs["authors"] = ["Paul Holzschuh", "Luis Maecker", "Taimur Khan", "Vitalii Kriukov"]
    ds.attrs["created_on"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    ds.attrs["history"] = "Created using code from the B-Cubed Hackathon 2024"

    #improvement - Assign the source attribute to ds
    if URL is not None and INPUT_PATH is not None:
        ds.attrs["source"] = URL + " | " + INPUT_PATH
    elif URL is not None:
        ds.attrs["source"] = URL
    elif INPUT_PATH is not None:
        ds.attrs["source"] = INPUT_PATH
            
    # Write the netcdf
    print("Dimensions of the netcdf to check coordinates:", ds.dims)
    print(ds)
    
    ds.to_netcdf(OUTPUT_PATH)
    print("\nNetCDF file written to", OUTPUT_PATH)

    # For further work with GEOTIFF:
    # variable_names = ['yearmonth','eeacellcode']   
    # Convert coordinates to a dictionary format
    # ds_coords_dict = {}
    # for coord_name, coord_data in ds.coords.items():
    #    ds_coords_dict[coord_name] = tuple(coord_data.values)

    #rds = rioxarray.open_rasterio(OUTPUT_PATH, masked=True, variable=variable_names)
    # rds.rio.to_raster(OUTPUT_PATH)

    
    
    # Remove the zip file and the data folder
    os.remove("data.zip")
    shutil.rmtree("data") 


# If the input file was provided, read the file
else:
    print("\nReading GBIF Data Cube from", INPUT_PATH)

    # Read the GBIF Data Cube
    df = pd.read_csv(INPUT_PATH, encoding="utf-8", sep="\t", index_col=False)

    # Apply the function to the text_column and create a new column
    df['east_number'] = df['eeacellcode'].apply(lambda x: extract_east_number(x))
    df['north_number'] = df['eeacellcode'].apply(lambda x: extract_north_number(x))

    ## get final coordinate: - for 1000m reslolution:
    df['east_coord_epsg3035_m'] = df['east_number'] * 1000
    df['north_coord_epsg3035_m'] = df['north_number'] * 1000

    # Write the GBIF Data Cube to a Geotiff file
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
            print("Dimensions in the dataset:", ds.dims)

    # Add attributes to the Geotiff file
    ds.attrs["title"] = "GBIF Data Cube"
    ds.attrs["authors"] = ["Paul Holzschuh", "Luis Maecker", "Taimur Khan", "Vitalii Kriukov"]
    ds.attrs["created_on"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    ds.attrs["history"] = "Created using code from the B-Cubed Hackathon 2024"

    #improvement - Assign the source attribute to ds
    if URL is not None and INPUT_PATH is not None:
        ds.attrs["source"] = URL + " | " + INPUT_PATH
    elif URL is not None:
        ds.attrs["source"] = URL
    elif INPUT_PATH is not None:
        ds.attrs["source"] = INPUT_PATH


    # Write the netcdf file
    print("Dimensions of the netcdf to check coordinates:", ds.dims)
    print(ds)
 
    ds.to_netcdf(OUTPUT_PATH)
    
    
    # For further work with GeoTIFF
    # variable_names = ['yearmonth', 'eeacellcode']
    # Convert coordinates to a dictionary format
    #ds_coords_dict = {}
    #for coord_name, coord_data in ds.coords.items():
    #    ds_coords_dict[coord_name] = tuple(coord_data.values)

    # rds = rioxarray.open_rasterio(OUTPUT_PATH, masked=True, variable=variable_names)
    # rds.rio.to_raster(OUTPUT_PATH)

    print("\nNetCDF file written to", OUTPUT_PATH)
