import geopandas as gpd

#Project to ITM CRS to create buffers/polygons and create GeoDataFrame and convert back to CRS4326 for addition to map
def create_buffers(venues, distance =10000):
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
        left_on='DZ_CODE',
        right_on='DZ2021_cd',
    )

#spatial join

