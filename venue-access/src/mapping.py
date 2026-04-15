import webbrowser
import os
import pandas as pd
import geopandas as gpd
import folium


#access venue shp file
venues = gpd.read_file('output/Venue Addresses.shp')

#create map of n.i.
m = folium.Map(location=(54.7877, -6.4923))


#add venue markers to map
venues.explore (
                m=m,
                marker_type= 'marker',
                popup=['Venue Name'],
                legend=False)

#Project to ITM CRS to create buffers/polygons
venues_proj = venues.to_crs(epsg=2157)
venue_buffer = venues_proj.buffer(10000)

#create GeoDataFrame and convert back to CRS4326 for addition to map
buffer_gdf = gpd.GeoDataFrame(geometry=venue_buffer, crs=2157)
buffer_web = buffer_gdf.to_crs(epsg=4326)

#prevent overlapping areas from being counted twice
buffers_union = buffer_gdf.dissolve()

buffer_web.explore(
    m=m,
    style_kwds={'color': 'red', 'fillOpacity': 0.3},
    name='5km Buffers'
)




