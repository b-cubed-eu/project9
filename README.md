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
