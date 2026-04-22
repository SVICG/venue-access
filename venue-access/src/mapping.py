import folium
import branca.colormap as cm
import numpy as np
from pandas.core.interchange import column


#create map of n.i.

def create_map(venues, buffer_union, population):
    m = folium.Map(location=(54.7877, -6.4923))

    # creating the custom ramp


    step = cm.LinearColormap(
 ["r", "y","g", "b" ],
        vmin=population['Population'].min(),
        vmax=population['Population'].max(),
        index=[
            1042,  # 0-20% of value range
            1843,  # 20%
            # 2645,  # 40%
            3447,  # 60%  # 80%
            4249  # 100%
        ],

        caption='Population'
        )

    folium.GeoJson(
        population.to_crs(epsg=4326),
        style_function=lambda feature: {
            'fillColor': step(feature['properties']['Population']),
            'fillOpacity': 0.7,
            'color': 'black',  # border color for the color fills
            'weight': 1,  # how thick the border has to be
            'dashArray': '5, 3'  # dashed lines length,space between them
        }
    ).add_to(m)
    step.add_to(m)

    #Choropleth map with population
    # folium.Choropleth(
    #     geo_data=population.to_crs(epsg=4326),
    #     data = population,
    #     columns=['DZ2021_cd', 'Population'],
    #     key_on='feature.properties.DZ2021_cd',
    #     fill_color = 'YlGnBu',
    #     bins=8,
    #     fill_opacity = 0.7,
    #     line_opacity = 0.2,
    #     legend_name = 'Population Density (per ha)',
    #     name = 'Population Density'
    # ).add_to(m)

    uncovered = population[~population['covered']].to_crs(epsg=4326)

    #Areas unengaged
    folium.GeoJson(
        uncovered,
        name = 'Uncovered Areas',
        style_function=lambda x: {
            'weight': 0.25,
            'fillColor': 'none',
            'color':'red'
        },
        tooltip = folium.GeoJsonTooltip(
            fields=['SDZ2021_nm', 'Population', 'pop_density'],
            aliases=['Data Zone', 'Population', 'Population Density (per ha)']
        )

    ).add_to(m)

    #add venue markers to map
    venues.explore (
                m=m,
                marker_type= 'marker',
                popup=['Venue Name'],
                legend=False
                    )
    #convert to lat/long for web map
    buffer_web = buffer_union.to_crs(epsg=4326)
    #add buffers
    buffer_web.explore(
    m=m,
    style_kwds={'color': 'blue', 'fillOpacity': 0.0},
    name='5km Buffers'
    )

    # #add population coverage
    # pop_web = population.to_crs(epsg=4326)
    # pop_web.explore(
    #     m=m,
    #     column = 'covered',
    #     cmap='Set1',
    #     legend=True,
    #     name = 'Population Coverage'
    # )


    folium.LayerControl().add_to(m)

    return m




