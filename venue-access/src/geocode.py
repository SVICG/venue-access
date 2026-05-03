import os
import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


#load data folders
data_folder = '../data/raw/'
output_folder = '../data/processed'

#access data file
data_file = 'Venue Addresses.xlsx'
data_file_path = os.path.join(data_folder, data_file)
address_df = pd.read_excel(data_file_path)

#concatenate address fields and save to new column, replacing empty cells.
address_df['Full_Address'] = (

    address_df['Street Address'].fillna('') + ', ' +
    address_df['Street Address 2'].fillna('') + ', ' +
    address_df['City'].fillna('') + ', ' +
    address_df['County'].fillna('') + ', ' +
    address_df['Postal Code'].fillna('')
                              )

#Ensure only 1 request per second
locator = Nominatim(user_agent='SVICG', timeout=10)
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

#run the geocode function on each address and save to a new column
address_df['location'] = address_df['Full_Address'].apply(geocode)

#extract latitude and longitude from location data into separate column
#returns none if no lat/long
address_df['latitude'] = address_df['location'].apply(lambda loc: loc.latitude if loc else None)
address_df['longitude'] = address_df['location'].apply(lambda loc: loc.longitude if loc else None)

#save and print amount and any failed addresses
failed = address_df[address_df['location'].isna()]
print(f"{len(failed)} addresses failed to geocode:")
print(failed[['Venue Name', 'Full_Address']])

#drop failed addresses
address_df = address_df[address_df['location'].notna()]

#create column for point data
geometry = gpd.points_from_xy(address_df['longitude'], address_df['latitude'])

#Define the coordinate CRS and convert into a GeoDataFramework
address_gdf = gpd.GeoDataFrame(address_df, crs='EPSG:4326', geometry=geometry)

#save as shp file
output_file = 'Venue Addresses.shp'
output_file_path = os.path.join(output_folder, output_file)
address_gdf.to_file(filename=output_file_path)
