import webbrowser
import os
import pandas as pd
import geopandas as gpd
import folium


venues = gpd.read_file('output/Venue Addresses.shp')

#create a map
output_file = "map2.html"
m = folium.Map(location=(54.7877, -6.4923))


print(venues.crs)
print(venues[['Venue Name', 'geometry']].head())
#add venue markers to map
venues.explore (
                m=m,
                marker_type= 'marker',
                popup=['Venue Name'],
                legend=False)



m.save(output_file)
webbrowser.open(output_file, new=2)  # open in new tab