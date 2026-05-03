# venue-access

This project has been developed to analyse the audience reach of the NI Science Festival and the  regions in Northern Ireland that are underserved by festival events. 

## Pre-requisites

To use the program ensure that git and conda are installed on your computer. 

You can download git from the official download site. - https://git-scm.com/downloads

Conda can be installed through Anaconda Navigator - https://www.anaconda.com/download/success

## Clone the repository 
The venue-access repository is hosted at: https://github.com/SVICG/venue-access

First fork the repository to your account and then clone your fork using the following command:

`git clone https://github.com/{your_username}/venue-access.git`



## Create the conda environment 
This can be set up via Anaconda Navigator or from the terminal.
If using Anaconda Navigator, select Import  from the Environments panel and install the environment.yml provided in the repository.

If setting up the environment via the terminal run the following command:

`conda env create -f environment.yml`

**The packages required are:**

 `geopandas`: for working with spatial vector data (https://geopandas.org/en/stable/)</br>
 `folium`: for creating interactive HTML maps (https://python-visualization.github.io/folium/latest/)<br>
 `pandas`: provides data structures (https://pandas.pydata.org/)</br>
 `branca`: for generating colour maps (https://python-visualization.github.io/branca/colormap.html)</br>
 `geopy`: for geocoding services and adding location to data (https://github.com/geopy/geopy)


## Required Data

### Venue Data

Venue locations should be provided as a CSV file and saved to:</br>
_venue-access/data/processed/venues.csv_ 

Venue data based on the NI Science Festival event locations has been provided.

If providing new data the CSV file must contain the following columns:

| Column     | Data Type | Required | Description                    |
|------------|-----------|----------|--------------------------------|
| Venue Name | String | Yes | Name of venue or location      |
| Street Address | String | Yes | Street Address and Number      |
| Street Address 2 | String | No | Additional street information |
| City | String | No | City venue is located          | 
| County | String | No | County venue is located        |
| Postal Code | String | Yes | Post code of venue or location |


Venue coordinates will be generated during processing.


### Population data

Population data has been provided and is sourced from the Northern Ireland Statistics and Research Agency (NISRA). The most current population estimates have been used which are the 2024 mid-year population estimates for Super Data Zones. </br>
This data can be found at: [Super Data Zones](https://www.nisra.gov.uk/publications/2024-mid-year-population-estimates-small-geographical-areas-within-northern-ireland) or downloaded via this [direct link](https://www.nisra.gov.uk/system/files/statistics/2025-12/MYE24_SDZ.xlsx).</br>
If providing alternative population data, this must be provided as a CSV as saved to: </br>
**_venue-access/data/processed/PopulationData.csv_**

Required columns are:

| Column    | Data Type | Required | Description                                               |
|-----------|-----------|----------|-----------------------------------------------------------|
| Area_code | string    | Yes      | NISRA area code linked to the Super Data Zone geographies |
| MYE       | float     | Yes      | Mid-year population estimate                              |

Population geometry will be taken from the Super Data Zone Shapefile. 


### Geographies

Super data zones are statistical output geographies designed to support low level census data such as the population estimates used in this project. 
The ESRI Shapefile for the Super Data Zone boundaries can be found here: https://www.nisra.gov.uk/publications/super-data-zone-boundaries-gis-format

## Running the programme
There are three scripts to run as part of this programme, they can all be found in:
_venue-access/src_

They should be run in the following order:

+ `geocode.py` - Geocodes the venue addresses and generates shapefile
+ `data_extra.py` - Extracts the required population data from the census file.
+ `main.py` - Runs the spatial analysis and generates the interactive map

The output will be saved to _venue-access/output/map.html_ and can be opened in a web browser.

