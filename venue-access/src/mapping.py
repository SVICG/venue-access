import folium
import branca.colormap as cm

#create map of n.i.

def create_map(venues, population):
    m = folium.Map(location=(54.7877, -6.4923))

    # creating the custom ramp
    step = cm.LinearColormap(
        ['green', 'yellow', 'orange', 'red'],
        vmin=population['underserved_score'].min(),
        vmax=population['underserved_score'].max(),
        caption='Underserved Score (Distance x Population)'
    )

    folium.GeoJson(
        population.to_crs(epsg=4326),
        name='Data Zones',
        style_function=lambda feature: {
            'fillColor': step(feature['properties']['underserved_score']),
            'fillOpacity': 0.7,
            'color': 'black',  # border color for the color fills
            'weight': 0.5,  # how thick the border has to be
            'dashArray': '5, 3'  # dashed lines length,space between them
        },

        #Tooltip to show data for each zone
        popup=folium.GeoJsonPopup(
            fields =['SDZ2021_nm', 'Population', 'nearest_venue_km'],
            aliases=['Data Zone', 'Population', 'Distance to nearest venue (km)' ],
        )
    ).add_to(m)
    step.add_to(m)

    #add venue markers to map

    folium.GeoJson(
        venues.to_crs(epsg=4326),
        marker=folium.Marker(icon=folium.Icon()),
        popup=folium.GeoJsonPopup(
            fields=['Venue Name','Full_Addre', 'buffer_population'],
            aliases=['Venue Name', 'Address', 'Population within 5km']
        ),
        name='Venues'
    ).add_to(m)


    folium.LayerControl().add_to(m)

    return m




