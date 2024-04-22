---
title: 'Species Occurrence Cube Portability'
tags:
  - invasive species
  - citizen science
  - automated image recognition
  - Isodontia mexicana
authors:
  - name: Andrew Rodrigues
    orcid: 0000-0003-2244-1002
    affiliation: 1
  - name: Anahita Kazem
    orcid: 0000-0003-1116-3385
    affiliation: 2
  - name: Taimur Khan
    orcid: 0000-0002-0596-5376
    affiliation: 3  
  - name: Luis Maecker
    orcid: 0000-0001-5233-5441
    affiliation: 4  
  - name: Ivette Serral Montoro
    orcid: 0000-0001-7484-9267
    affiliation: 6   
  - name: Vitalii Kriukov
    orcid: 0000-0001-7484-9267
    affiliation: 5  
  - name: Paul
    orcid: 0000-0001-7484-9267
    affiliation: 4  
    
affiliations:
 - name: Global Biodiversity Information Facility, Universitetsparken 15, DK-2100 Copenhagen, Denmark
   index: 1
 - name: German Centre for Integrative Biodiversity Research (iDiv), Halle-Jena-Leipzig, Puschstrasse 4, 04103 Leipzig, Germany
   index: 2
 - name: Helmholtz Centre for Environmental Research - UFZ, Theodor-Lieser-Str. 4, 06120 Halle, Germany 
   index: 3
 - name: Faculty of Physics and Earth System Sciences, University of Leipzig, Linnéstraße 5, 04103 Leipzig
   index: 4
 - name: School of Engineering and Applied Science, Aston University  B4 7ET Birmingham, United Kingdom
   index: 5
 - name: CREAF,Campus de Bellaterra (UAB) Edifici C, 08193 Cerdanyola del Vallès, Spain
   index: 6
 

date: 05. April 2024
bibliography: paper.bib
authors_short: Rodrigues et al.
group: Species occurence cube portability
event: B-Cubed Hackathon, Brussels, 2024
biohackathon_name: Alien-CSI Hackathon, Brussels, 2024
biohackathon_url: https://alien-csi.eu/
biohackathon_location: Brussels, Belgium
---

# Introduction

The increasing recognition of the need for Essential Biodiversity Variables (EBVs), a set of key components of biodiversity, which when monitored should allow for the tracking of the status of all the elements of biodiversity, requires that biodiversity data is provided in a format that allows for the easy combination with sensor-detected environmental variables. Data cubes have become a standard within the atmospheric sciences for the calculation of Essential Climate Variables (ECVs) the climate equivalent of EBVs used for climate reporting, where the Network Common Data Form (Unidata, 2023) - NetCDF - has become the standard format for storing this type of data.  NetCDFs can store multidimensional data such as temperature, wind speed, salinity, pH in the form of array that can then be diplayed through a dimension such as time.  The format is self-describing with the file containing information about the data it contains and portable allowing computer with different ways of storing integers, characters and floating point numbers to access the file. 

GBIF - the Global Biodiversity Information Facility - currently provides users to the ability to search and query its database using user-defined filters via its APIs that allow for download occurrence data or species lists as tab delimited CSVs. GBIF aims to provide its data in a cube-like format allowing users to aggregate species occurrence counts using user defined dimensions and user-specified grids. These data will then be provided to users in a CSV format. CSV is a data exchange format for tabular data that is most commonly used for the exchange of data between database and spreadsheet programs and does not lend itself to these new data cubes where formats that better handle raster data may be more appropriate.

In this project, we aimed to provide a python package that allows users to create cube downloads in NetCDF and ensure that the new GBIF data cubes could be more efficently used in the calculation of Essential Biodievrsity Variables.  We also wanted to explore the production of these cubes in other formats starting with GeoTIFF and Cloud-Optimized GeoTIFF (COG), the TIFF format a commonly used format in geospatial analyses for raster data.  We also wanted to explore user needs by surveying data cube users at the B-Cubed Hackathon to develop a prioritized selection of data formats that should be considered for developement in the future. 

## Survey Results
27 B-cubed hackathon participants attempted to complete the survey of 11 questions (Appendix 1), 20 of which completed the survey.  Dependent on the question, reponses could be single choice, multiple choice and free text meaning that summmed responses for some questions were over 20 responses.  The top research areas of participants were in ecology and biodiversity studies and informatics and over fifty percent had had no experience using data cubes in the past.  Participants expressed desires to use data cubes in ecological modelling, determining trends over time, biodiversity indicators, Convention on Biological Diversity reporting, more efficient data harvesting and computing habitat connectivity.

![image](https://github.com/b-cubed-eu/project9/assets/31403807/5b51f95f-4ab4-453e-bea8-a43901c89771)


![image](https://github.com/b-cubed-eu/project9/assets/31403807/21e4af02-2eb3-40d0-9594-1400de9f2199)

Of those with no experience of data cubes, when asked why they had had no experience, responses included a lack of time, lack of knowledge of the existence of data cubes or a lack of understanding of the relevance of cubes to their work. 

Of those who had some familiarity with data cubes (12/26 respondents), 4 replied that had been using NetCDF formats, 2 with Zarr formats, 5 with CSV, 2 with GeoTIFF, 2 with Cloud-Optimised GeoTIFF (COG), 1 with TIFF and 1 with xarray. Reasons for using these formats included their portability, high computational performance, software compatability, availability and frequency of use among collaborators.

![image](https://github.com/b-cubed-eu/project9/assets/31403807/3e82f521-56d7-4904-bb9f-3d7e87a391ff)

The top 5 formats that were identified by all participants as preferred formats for species occurrence data cube in ranked order were: CSV, NetCDF, GeoTIFF and GeoJSON and Shapefile. 

### 


## gbif-csv2netcdf4 Converter

The gbif-csv2netcdf Converter is a Python-based utility designed to facilitate the transformation of biodiversity data from the GBIF (Global Biodiversity Information Facility) Data Cube format into the versatile NetCDF (Network Common Data Form) file format. This conversion process allows for more efficient storage, access, and analysis of large-scale environmental and biodiversity datasets. Developed during the B-Cubed Hackathon 2024, this tool stands as a pivotal development for researchers and scientists in the fields of ecology, climate science, and biodiversity conservation.

The script operates by either downloading a GBIF Data Cube from a specified URL or reading an existing local CSV file that was extracted from the GBIF database. Once the data cube is obtained, it processes the data to fit into the NetCDF format, enabling the use of dimensions for more organized and accessible data. The output is a NetCDF file that contains all the original data, now ready for analysis and visualization with tools that support this format.


## Discussion and conclusions
The CSV format remained the most popular format for the provision of data cubes to users and may reflect a familiarity with receiving GBIF-mediated data within a CSV format, the only format that GBIF downloads are currently provided. However, even among those users that had some familiarity with data cubes, the CSV format still ranked as the most popular format for providing species occurrence data cubes. The discussion of the desired format wiil depend ultimately on the intended use of the data. For most participants at the hackathon, species occurrence data cubes were a new concept, and understanding how these cubes could be used within other hackathon projects was a key element of their respective projects. Limited socialization of the species occurrence data cubes and the novel functionality that they allow i.e. the aggregation of species occurrence data using user-defined dimensions and grids, restricts user´s ability to identify a desired data format for the cubes. As researchers become more familiar with the virtues of the species occurrence data cube i.e. the kinds of analyses that they facilitate, we would expect clearer signals from a matured user community on data formats.  

One format that was clearly identified as one that was in widespread use was NetCDF and the python package gbif-csv2netcdf Converter provides users the ability to convert from csv to NetCDF. NetCDF was identified as the second most popular format,

# Acknowledgements

# Appendix 1
[GBIF.data.cube.survey_survey.outline.pdf](https://github.com/b-cubed-eu/project9/files/15039662/GBIF.data.cube.survey_survey.outline.pdf)


# References
H. M. Pereira et al., Essential Biodiversity Variables.Science339,277-278(2013).DOI:10.1126/science.1229931
Unidata,2024: NetCDF Users Guide  v1.1. Boulder, CO: UCAR/Unidata Program Center. https://doi.org/10.5065/D6H70CW6
https://techdocs.gbif.org/en/data-use/data-cubes

