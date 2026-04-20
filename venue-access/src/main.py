import geopandas as gpd
import pandas as pd
from analysis import create_buffers, dissolve_buffer, zone_population
from mapping import create_map


#access venue and population files
venues = gpd.read_file('../data/processed/Venue Addresses.shp')
data_zones = gpd.read_file('../data/raw/DZ2021.shp')
pop_df = pd.read_excel('../data/raw/NI2024PopulationData.xlsx')


#buffer functions
buffers = create_buffers(venues)
buffer_union = dissolve_buffer(buffers)

#join population and data zones
population = zone_population(data_zones, pop_df)

# print(population.head())
# print(population.shape)
# print(population[2024].isna().sum())


#map function
m = create_map(venues, buffer_union)



#save map
#m.save('../output/map.html')