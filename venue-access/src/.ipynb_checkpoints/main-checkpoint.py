import geopandas as gpd
import pandas as pd
from analysis import zone_population, population_density, calculate_underserved, venue_pop
from mapping import create_map


#access venue and population files
venues = gpd.read_file('../data/processed/Venue Addresses.shp')
data_zones = gpd.read_file('../data/raw/SDZ2021.shp')
pop_df = pd.read_csv('../data/processed/PopulationData.csv')


#join population and data zones
population = zone_population(pop_df, data_zones)


#calculate population density
population = population_density(population)
print(population.head())

population = calculate_underserved(population, venues)

venues = venue_pop(venues, population)

#map function
m = create_map(venues, population)

#save map
m.save('../output/map.html')