import folium

#create map of n.i.

def create_map(venues, buffer_union):
    m = folium.Map(location=(54.7877, -6.4923))
    #add venue markers to map
    venues.explore (
                m=m,
                marker_type= 'marker',
                popup=['Venue Name'],
                legend=False
                    )
    #convert to lat/long for web map
    buffer_web = buffer_union.to_crs(epsg=4326)

    buffer_web.explore(
    m=m,
    style_kwds={'color': 'red', 'fillOpacity': 0.3},
    name='10km Buffers'
    )

    folium.LayerControl().add_to(m)

    return m




