# Species Occurrence Cube Portability

### Project 9 @ B-Cubed Hackathon 2024 - Hacking Biodiversity Data Cubes for Policy.

### Technical Questions

### Deliverables

- User survey for cubes, to identify user needs (i.e. formats needed by users). Get results by E.O.W. (Anahita)
- BioHackrxiv paper (Andrew)
- Proof of concepts for NetCDF (Taimur, Paul, Luis) and COG-GeoTIFF (Vitalii)
- Create an endpoint in sensorthings API? A standard for describing observations. (Ivette)

> Stick to Open Geospatial Consortium standards.

> Open to any programming language.

> Perfect solutions not expected.

### Notes

- **NetCDF**: 
    - Script to convert from CSV to NetCDF4 is available as `gbif-csv2netcdf.py`.
    - The script can be used to convert a local CSV file or a download URL for a GBIF Cube to a NetCDF file.
    - The script has to be run from the command line and the arguments can be seen by running `python gbif-csv2netcdf.py -h`.
    - The script dependencies are in the `requirements.txt` file.
    - The script is a proof of concept and can be improved.
    - Sample GBIF Data Cube: https://api.gbif.org/v1/occurrence/download/request/0000025-240314170635999.zip


# Documentation: gbif-csv2netcdf4 Converter #
# Description #

The gbif-csv2netcdf Converter is a Python-based utility designed to facilitate the transformation of biodiversity data from the GBIF (Global Biodiversity Information Facility) Data Cube format into the versatile NetCDF (Network Common Data Form) file format. This conversion process allows for more efficient storage, access, and analysis of large-scale environmental and biodiversity datasets. Developed during the B-Cubed Hackathon 2024, this tool stands as a pivotal development for researchers and scientists in the fields of ecology, climate science, and biodiversity conservation.

# Workflow #

The script operates by either downloading a GBIF Data Cube from a specified URL or reading an existing local CSV file that was extracted from the GBIF database. Once the data cube is obtained, it processes the data to fit into the NetCDF format, enabling the use of dimensions for more organized and accessible data. The output is a NetCDF file that contains all the original data, now ready for analysis and visualization with tools that support this format.


![](workflow.png)


Steps:

Preparation: Ensure Python 3.11.7 is installed, and set up a virtual environment.

    pip -m venv venv && source venv/bin/activate

Installation: Install required dependencies as listed in the requirements.txt file.

    pip install -r requirements.txt


Execution: Run the script with the appropriate command-line arguments to specify the input source (URL or local file), dimensions, output path, projection, and a digital object identifier (doi).

    python gbif-csv2netcdf.py -i <input_path> -u <url> -d <dimensions> -o <output> -p <projection> -doi <doi> -c <compression>

Example:
    
        python gbif-csv2netcdf.py -u https://api.gbif.org/v1/occurrence/download/request/0000025-240314170635999.zip -d "time,lat,lon" -o output.nc -p EPSG:3035 -doi 10.5281/zenodo.123456 -c True

**Argument types and definitions**

    -i, --input: Path to the local CSV file to be converted to NetCDF.
    -u, --url: URL to download the GBIF Data Cube in ZIP format.
    -d, --dimensions: Dimensions to be used in the NetCDF file (e.g., "time,lat,lon").
    -o, --output: Path to the output NetCDF file.
    -p, --projection: Projection to be used in the NetCDF file (default =  "EPSG:3035").
    -doi, --doi: Digital Object Identifier (DOI) for the NetCDF file.
    -c, --compression: Enable or disable compression for the NetCDF file (True or False).
    --grid-code-column: Specifies the column name for EEA grid

# About NetCDF File Format #

NetCDF (Network Common Data Form) is a set of software libraries and machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data. This format is widely used in the scientific community for storing and distributing scientific data. It is particularly suited for handling large volumes of data in a way that is efficient both in terms of storage and computational access.
Data Cubes Concept

# About Data Cubes #

Data Cubes are a method of structuring data in multiple dimensions (usually three or more) to enable efficient querying and analysis. This concept is especially useful in the field of remote sensing, climate and environmental data analysis, and GIS applications, where data is inherently multi-dimensional (e.g., spatial, temporal, and spectral dimensions). Data cubes facilitate complex data analysis tasks, such as trend analysis over time or spatial pattern recognition, by providing a structured and intuitive way to handle multidimensional datasets.

General Information

    Authors: Paul Holzschuh, Luis Maecker, Taimur Khan
    License: MIT
    Python Version Required: 3.11.7
    Dependencies: xarray, numpy, pandas, wget, zipfile, shutil, time, geopandas
    Sample Dataset: https://api.gbif.org/v1/occurrence/download/request/0000025-240314170635999.zip

# Documentation: gbif-2geotiff Converter #
### Description ###
@vitalii you can add your documentation part here!

