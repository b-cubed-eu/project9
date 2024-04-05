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
group: Project 9: Species Occurence Cube Portability
event: B-Cubed Hackathon, Brussels, 2024
biohackathon_name: B-Cubed Hackathon, Brussels, 2024
biohackathon_url: https://alien-csi.eu/](https://b-cubed.eu/b-cubed-hackathon
biohackathon_location: Brussels, Belgium
---

# Introduction

The ability to handle spatio-temporal biodiversity data is critical if we are to effectively monitor trends in biodiversity over time. Data cubes have become a standard within the atmospheric sciences, where the Network Common Data Form - NetCDF - allow users to slice data in whichever dimensions the user demands and come with well developed metadata standards.  They and have become a standard for the calculation of Essential Climate Variables that are used in climate reporting and monitoring. With similar approaches being adopted by the biodiversity community in the form of Essential Biodiversity Variables - those key components of biodiversity that can be used to elucidate biodiversity patterns and trends - calculation of these variables requires that biodiversity data is packaged in a similar way that allows for its interoperability with other relevant environmental datasets to allow the complex geospatial analyses required.  

GBIF - the Global Biodiversity Information Facility - currently provides its three download options - simple, Darwin Core Archive and Species List - as tab delimited CSVs and will provide its newest download format the "data cube" format in the same format. These new aggregated data cube formats that aggregate measures of biodiversity, typically species occurrence counts, using user-specified grids. CSV is a data exchange format for tabular data that is most commonly used for the exchange of data between database and spreadsheet programs and does not lend itself to these new data cubes where formats that rasterize the data may be more appropriate.

In this project, we aimed to provide a python package that allows users to create cube downloads in NetCDF and ensure that the new GBIF data cubes could be more efficently used in the calculation of Essential Biodievrsity Variables.  We also wanted to explore the production of these cubes in other formats starting with GeoTIFF and Cloud-Optimized GeoTIFF (COG), the TIFF format a commonly used format in geospatial analyses for raster data.  We also wanted to explore user needs by surveying data cube users at the B-Cubed Hackathon to develop a prioritized selection of data formats that should be considered for developement in the future. 

## ...... Package



## Survey Results
### 


## Discussion and conclusions



# Acknowledgements

# References





