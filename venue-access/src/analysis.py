import geopandas as gpd
import pandas as pd

#Project to ITM CRS to create buffers/polygons and create GeoDataFrame and convert back to CRS4326 for addition to map
def create_buffers(venues, distance =5000):
    venues_proj = venues.to_crs(epsg=2157)
    venue_buffer = venues_proj.buffer(distance)
    buffer_gdf = gpd.GeoDataFrame(geometry=venue_buffer, crs=2157)
    return buffer_gdf

#prevent overlapping areas from being counted twice
def dissolve_buffer(buffer_gdf):
    return buffer_gdf.dissolve()

#merge population with datazones
def zone_population(population, data_zones):
    return data_zones.merge(
        population,
        left_on= 'SDZ2021_cd',
        right_on= 'DZ_CODE',
    )

#spatial join population and data areas
def join_population(population, buffer):
    population = population.to_crs(epsg=2157)
    joined_pop = gpd.sjoin(population, buffer, how='inner', predicate='intersects')
    return joined_pop

#calculate population density
def population_density(population):
    population['pop_density'] = population['Population'] / population['Area_ha']
    return population

#create areas of coverage for map
def coverage(population, buffer):
    population = population.to_crs(buffer.crs)
    population['covered'] = population.intersects(buffer.geometry.iloc[0])
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

    return pop_proj



