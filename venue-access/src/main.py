import geopandas as gpd
from analysis import create_buffers, dissolve_buffer
from mapping import create_map


#access venue shp file
venues = gpd.read_file('../data/processed/Venue Addresses.shp')

#buffer functions
buffers = create_buffers(venues)
buffer_union = dissolve_buffer(buffers)

#map function
m = create_map(venues, buffer_union)

#save map
m.save('../output/map.html')