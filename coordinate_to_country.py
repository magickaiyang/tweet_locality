# multiprocessing enabled, each process will hold a connection to the sql server
import ogr
import pyodbc
import rtree
import multiprocessing

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

# Rtree spatial index
index = rtree.index.Index(interleaved=False)
for fid in range(0, layer.GetFeatureCount()):
        feature = layer.GetFeature(fid)
        geometry = feature.GetGeometryRef()
        xmin, xmax, ymin, ymax = geometry.GetEnvelope()
        index.insert(fid, (xmin, xmax, ymin, ymax))

server = '128.46.137.201'
database = 'LOCALITY1'
username = 'localityedit'
password = 'Edit123'
cnxn2 = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor2 = cnxn2.cursor()


def locate_country(lon, lat, sql_table_id):
    # Transform incoming longitude/latitude to the shapefile's projection
    [lon, lat, z] = coordinate_transformer.TransformPoint(lon, lat)

    # Create a point
    pt = ogr.Geometry(ogr.wkbPoint)
    pt.SetPoint_2D(0, lon, lat)

    country = ''

    xmin, xmax, ymin, ymax = pt.GetEnvelope()
    possible_countries = list(index.intersection((xmin, xmax, ymin, ymax)))

    # shortcut, if only one country left
    if len(possible_countries) == 1:
        country = layer.GetFeature(possible_countries[0]).GetFieldAsString(field_id)

    else:
        for fid in possible_countries:
            feature = layer.GetFeature(fid)
            geometry = feature.GetGeometryRef()
            if pt.Intersects(geometry):
                country = feature.GetFieldAsString(field_id)
                break



    query2 = "UPDATE [LOCALITY1].[dbo].[tweets] SET issued_in = '" + country + "' WHERE id = " + str(sql_table_id)
    print(query2)
    cursor2.execute(query2)
    cnxn2.commit()


#locate_country(-80.2358746, 26.224614, 1)
