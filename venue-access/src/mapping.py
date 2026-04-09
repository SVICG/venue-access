import webbrowser
import os
import pandas as pd
import geopandas as gpd
import folium

venues = gpd.read_file('venues.shp')


#create a map
output_file = "map2.html"
m = folium.Map(location=(54.7877, -6.4923))

m.save(output_file)
webbrowser.open(output_file, new=2)  # open in new tab