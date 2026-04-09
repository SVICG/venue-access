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

