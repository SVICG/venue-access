import os

import pandas as pd
import geopandas as gpd

#load data folders
data_folder = './data/'
output_folder = './output/'

#access data file
data_file = 'Venue Addresses.xlsx'
data_file_path = os.path.join(data_folder, data_file)
address_df = pd.read_excel(data_file_path)
print(address_df.head())

#concatenate address fields and save to new column, replacing empty cells.
address_df['Full_Address'] = (

    address_df['Venue Name'].fillna('') + ', ' +
    address_df['Street Address'].fillna('') + ', ' +
    address_df['Street Address 2'].fillna('') + ', ' +
    address_df['City'].fillna('') + ', ' +
    address_df['County'].fillna('') + ', ' +
    address_df['Postal Code'].fillna('')
                              )
