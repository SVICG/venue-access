import geopandas as gpd
import pandas as pd
from analysis import create_buffers, dissolve_buffer, zone_population, join_population, coverage, population_density
from mapping import create_map
import json

#access venue and population files
venues = gpd.read_file('../data/processed/Venue Addresses.shp')
data_zones = gpd.read_file('../data/raw/DZ2021.shp')
pop_df = pd.read_excel('../data/raw/NI2024PopulationData.xlsx')


#buffer functions
buffers = create_buffers(venues)
buffer_union = dissolve_buffer(buffers)

#join population and data zones
population = zone_population(pop_df, data_zones,)


#spatial join population within buffer
joined = join_population(population, buffer_union)

#calculate population
boundary_pop = joined['Population'].sum()
total_pop = population['Population'].sum()

print(boundary_pop, total_pop)

#match which datazones are covered with the buffer area
population = coverage(population, buffer_union)

#calculate population density
population = population_density(population)


#map function
m = create_map(venues, buffer_union, population)

#save map
m.save('../output/map.html')