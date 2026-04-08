import os
import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


#load data folders
data_folder = './data/'
output_folder = './output/'

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

locator = Nominatim(user_agent='SVICG', timeout=10)
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

address_df['location'] = address_df['Full_Address'].apply(geocode)

#gather latitude and longitude from location data
address_df['latitude'] = address_df['location'].apply(lambda loc: loc.latitude if loc else None)
address_df['longitude'] = address_df['location'].apply(lambda loc: loc.longitude if loc else None)

#create column for point data
geometry = gpd.points_from_xy(address_df['latitude'], address_df['longitude'])
address_gdf = gpd.GeoDataFrame(address_df, crs='EPSG:2157', geometry=geometry)

#save as shp file
output_file = 'Venue Addresses.shp'
output_file_path = os.path.join(output_folder, output_file)
address_gdf.to_file(filename=output_file_path)
