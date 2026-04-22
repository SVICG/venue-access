import folium
import branca.colormap as cm
from pandas.core.interchange import column


#create map of n.i.

def create_map(venues, buffer_union, population):
    m = folium.Map(location=(54.7877, -6.4923))

    # creating the custom ramp


    #Choropleth map with population
    folium.Choropleth(
        geo_data=population.to_crs(epsg=4326),
        data = population,
        columns=['DZ2021_cd', 'Population'],
        key_on='feature.properties.DZ2021_cd',
        fill_color = 'YlGnBu',
        bins=8,
        fill_opacity = 0.7,
        line_opacity = 0.2,
        legend_name = 'Population Density (per ha)',
        name = 'Population Density'
    ).add_to(m)

    uncovered = population[~population['covered']].to_crs(epsg=4326)

    #Areas unengaged
    folium.GeoJson(
        uncovered,
        name = 'Uncovered Areas',
        style_function=lambda x: {
            'weight': 0.25,
            'fillColor': 'none',
            'color':'orange'
        },
        tooltip = folium.GeoJsonTooltip(
            fields=['DZ2021_nm', 'Population', 'pop_density'],
            aliases=['Data Zone', 'Population', 'Population Density (per ha']
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




