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

    band_colours= {
        '<800m': 'green',
        '800m-2km': 'yellowgreen',
        '2km-5km': 'yellow',
        '5km-10km': 'orange',
        '>10km': 'red'
    }


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
            fields =['SDZ2021_nm', 'MYE', 'pop_density', 'nearest_venue_km'],
            aliases=['Data Zone', 'Population','Population Density (per ha)', 'Distance to nearest venue (km)' ],
        )
    ).add_to(m)
    step.add_to(m)

    #distance band layer
    folium.GeoJson(
        population.to_crs(epsg=4326),
        name='Distance Bands',
        show=False,
        style_function=lambda feature: {
            'fillColor': band_colours.get(feature['properties']['distance_band'], 'grey'),
            'fillOpacity': 0.7,
            'color': 'black',
            'weight': 0.5,
            'dashArray': '5, 3'
        },
        popup=folium.GeoJsonPopup(
            fields =['SDZ2021_nm', 'MYE', 'pop_density', 'nearest_venue_km', 'distance_band'],
            aliases=['Data Zone', 'Population', 'Population Density (per ha)', 'Distance to Nearest Venue (km)',
                     'Distance Band']
        )
    ).add_to(m)

    #add venue markers to map

    folium.GeoJson(
        venues.to_crs(epsg=4326),
        marker=folium.Marker(icon=folium.Icon()),
        popup=folium.GeoJsonPopup(
            fields=['Venue Name','Full_Addre', '5k_buffer_population', 'access_buffer_population'],
            aliases=['Venue Name', 'Address', 'Population within 5km', 'Population within 400m']
        ),
        name='Venues'
    ).add_to(m)


    folium.LayerControl().add_to(m)

    return m




