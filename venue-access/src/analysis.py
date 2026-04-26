import pandas as pd


#merge population with datazones
def zone_population(population, data_zones):
    """
    Merges population and data zone boundary files

    Parameters
    ----------
    population : pd.DataFrame
      Dataframe containing population data

    data_zones : gpd.GeoDataFrame
        GeoDataFrame containing NISRA Super Data Zone boundaries

    Returns
    -------
    gpd.GeoDataFrame
        merged gdf containing population data
    """
    return data_zones.merge(
        population,
        left_on= 'SDZ2021_cd',
        right_on= 'Area_code',
    )

#calculate population density based on 'MYE'(Mid-Year Estimates)
def population_density(population):
    """
    Calculates population density based on Mid-Year Estimates (MYE)

    Parameters
    ----------
    population : gpd.GeoDataFrame
        GeoDataFrame containing population data with relevant 'MYE' and 'Area_ha' columns

    Returns
    population : gpd.GeoDataFrame
        GeoDataFrame with new 'pop_density' column (people per hectar)
    """
    population['pop_density'] = population['MYE'] / population['Area_ha']
    return population


#Map zones weighted by population
def calculate_underserved(population, venue):
    """
    Calculates a weighted score for underserved datazones. Score is based on distance to the nearest venue weighted by population.

    Parameters
    ----------
    population : gpd.GeoDataFrame
        GeoDataFrame containing population data

    venue : gpd.GeoDataFrame
        GeoDataFrame containing venue data and point location

    Returns
    -------
    pop_proj : gpd.GeoDataFrame
        GeoDataFrame containing additional columns: nearest_venue, distance_band, underserved_score, nearest_venue_km

    """
    #Project to Irish Transverse Mercator to calculate distance in metres
    pop_proj = population.to_crs(epsg=2157)
    venue_proj = venue.to_crs(epsg=2157)

    #Save central point of each polygon to a new 'centroid' column
    pop_proj['centroid'] = pop_proj['geometry'].centroid

    #Save distance to nearest venue in metres
    pop_proj['nearest_venue'] = pop_proj['centroid'].apply(
        lambda point: venue_proj.distance(point).min()
    )

    #Group distances into categories. Use float('inf') for unbound upper value
    bins = [0, 800, 2000, 5000, 10000, float('inf')]
    labels = ['<800m', '800m-2km', '2km-5km', '5km-10km', '>10km' ]
    pop_proj['distance_band'] = pd.cut(
        pop_proj['nearest_venue'], bins=bins, labels=labels
    )

    #Multiple population by distance tro give a weighted score
    pop_proj['underserved_score'] = pop_proj['nearest_venue']* pop_proj['MYE']

    #convert to km and remove decimal places for map data
    pop_proj['nearest_venue_km'] = (pop_proj['nearest_venue']/1000).round(2)

    #drop centroid column as no longer needed
    pop_proj = pop_proj.drop(columns=['centroid'])

    return pop_proj


#Calculate population around venues

def venue_pop(venues, population):
    """
    Calculates the population within a 5km radius of a venue

    Parameters
    ----------
    venues : gpd.GeoDataFrame
        GeoDataFrame containing Venue data

    population : gpd.GeoDataFrame
        GeoDataFrame containing population data

    Returns
    -------
    venue_proj : gpd.GeoDataFrame
        GeoDataFrame containing venue data with an additional column (buffer_population) showing population within a 5km radius of the venue.

    """
    # Project to ITM CRS to create buffers in meters
    pop_proj = population.to_crs(epsg=2157)
    venue_proj = venues.to_crs(epsg=2157)

    #create 5km buffer
    buffers = venue_proj.copy()
    venue_proj['buffer'] = venue_proj.buffer(5000)

    venue_proj['buffer_population'] = venue_proj['buffer'].apply(
        lambda geom: pop_proj[pop_proj.intersects(geom)]['MYE'].sum()
    )

    # drop buffer column as no longer needed
    venue_proj = venue_proj.drop(columns=['buffer'])

    return venue_proj