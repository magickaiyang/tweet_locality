# multiprocessing enabled, each process will hold a connection to the sql server
import ogr
import pyodbc
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

server = '128.46.137.201'
database = 'LOCALITY1'
username = 'localityedit'
password = 'Edit123'
cnxn2 = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor2 = cnxn2.cursor()


def locate_country(lon, lat, index):
    # Transform incoming longitude/latitude to the shapefile's projection
    [lon, lat, z] = coordinate_transformer.TransformPoint(lon, lat)

    # Create a point
    pt = ogr.Geometry(ogr.wkbPoint)
    pt.SetPoint_2D(0, lon, lat)

    # Set up a spatial filter such that the only features we see when we
    # loop through "layer" are those which overlap the point defined above
    layer.SetSpatialFilter(pt)

    country = ''
    # will execute only once
    for entry in layer:
        country = entry.GetFieldAsString(field_id)

    # print('latitude: ', str(latitude), 'longitude:', str(longitude), 'country: ', country)
    query2 = "UPDATE [LOCALITY1].[dbo].[tweets] SET issued_in = '" + country + "' WHERE id = " + str(index)
    print(query2 + str(multiprocessing.current_process()))
    cursor2.execute(query2)
    cnxn2.commit()

# print(locate_country(-82.44074796, 38.42133044))
