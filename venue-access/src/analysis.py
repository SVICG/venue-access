import pandas as pd

#merge population with datazones
def zone_population(population, data_zones):
    return data_zones.merge(
        population,
        left_on= 'SDZ2021_cd',
        right_on= 'DZ_CODE',
    )

#calculate population density
def population_density(population):
    population['pop_density'] = population['Population'] / population['Area_ha']
    return population


#Map zones weighted by population

def calculate_underserved(population, venue):
    pop_proj = population.to_crs(epsg=2157)
    venue_proj = venue.to_crs(epsg=2157)

    #get centroid
    pop_proj['centroid'] = pop_proj['geometry'].centroid

    #find nearest venue to each data zone
    pop_proj['nearest_venue'] = pop_proj['centroid'].apply(
        lambda point: venue_proj.distance(point).min()
    )

    #create distance categories
    bins = [0, 800, 2000, 5000, 10000, float('inf')]
    labels = ['<800m', '800m-2km', '2km-5km', '5km-10km', '>10km' ]
    pop_proj['distance_band'] = pd.cut(
        pop_proj['nearest_venue'], bins=bins, labels=labels
    )

    #weighted by distance
    pop_proj['underserved_score'] = pop_proj['nearest_venue']* pop_proj['Population']

    #convert to km and remove decimal places for map data
    pop_proj['nearest_venue_km'] = (pop_proj['nearest_venue']/1000).round(2)

    #drop centroid column
    pop_proj = pop_proj.drop(columns=['centroid'])

    return pop_proj


#Calculate population around venues

def venue_pop(venues, population):
    # Project to ITM CRS to create buffers
    pop_proj = population.to_crs(epsg=2157)
    venue_proj = venues.to_crs(epsg=2157)

    #create 5km buffer
    buffers = venue_proj.copy()
    buffers['geometry'] = venue_proj.buffer(5000)

    venue_proj['buffer_population'] = buffers['geometry'].apply(
        lambda geom: pop_proj[pop_proj.intersects(geom)]['Population'].sum()
    )

    return venue_proj