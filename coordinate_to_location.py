import ogr

driver = ogr.GetDriverByName('ESRI Shapefile')
shapefile = driver.Open("maps/world_countries_2017.shp")  # open the shapefile
layer = shapefile.GetLayer(0)  # Get the shapefile's first layer

# field, name of the country
field_id = layer.GetLayerDefn().GetFieldIndex("CNTRY_NAME")
# The following assumes that the latitude longitude is in WGS84
# This is identified by the number "4326", as in "EPSG:4326"
# We will create a transformation between this and the shapefile's
# project, whatever it may be
geo_ref = layer.GetSpatialRef()
point_ref = ogr.osr.SpatialReference()
point_ref.ImportFromEPSG(4326)
coordinate_transformer = ogr.osr.CoordinateTransformation(point_ref, geo_ref)


def locate_country(lon, lat):
    # Transform incoming longitude/latitude to the shapefile's projection
    [lon, lat, z] = coordinate_transformer.TransformPoint(lon, lat)

    # Create a point
    pt = ogr.Geometry(ogr.wkbPoint)
    pt.SetPoint_2D(0, lon, lat)

    # Set up a spatial filter such that the only features we see when we
    # loop through "layer" are those which overlap the point defined above
    layer.SetSpatialFilter(pt)

    # will execute only once
    for entry in layer:
        return entry.GetFieldAsString(field_id)

    # no hit
    return ''

#print(locate_country(-82.44074796, 38.42133044))
