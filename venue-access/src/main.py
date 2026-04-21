import geopandas as gpd
import pandas as pd
from analysis import create_buffers, dissolve_buffer, zone_population, join_population
from mapping import create_map


#access venue and population files
venues = gpd.read_file('../data/processed/Venue Addresses.shp')
data_zones = gpd.read_file('../data/raw/DZ2021.shp')
pop_df = pd.read_excel('../data/raw/NI2024PopulationData.xlsx')


#buffer functions
buffers = create_buffers(venues)
buffer_union = dissolve_buffer(buffers)

#join population and data zones
population = zone_population(pop_df, data_zones,)


print(type(population))
print(population.head())


#spatial join population within buffer
joined = join_population(population, buffer_union)

#calculate population
# boundary_pop = joined['population'].sum()
# total_pop = population['population'].sum()

#map function
m = create_map(venues, buffer_union)



#save map
#m.save('../output/map.html')