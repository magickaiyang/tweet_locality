from shapely.geometry import Point, Polygon
import shapefile

myshp = open("C:/Users/Shoto/PycharmProjects/LocalityTweets/venv/shapefiles/tl_2017_us_state.shp", "rb")
mydbf = open("C:/Users/Shoto/PycharmProjects/LocalityTweets/venv/shapefiles/tl_2017_us_state.dbf", "rb")
r = shapefile.Reader(shp=myshp, dbf=mydbf)

# print r.numRecords

# for i in range(r.numRecords):
#     print r.record(i)

test_coord = Point(-86.990100, 40.332937)

# feature = r.shapeRecords()[0]
# coords = feature.shape.__geo_interface__
# print coords['coordinates']

# for i in range(r.numRecords):
#     feature = r.shapeRecords()[i]
#     coords = feature.shape.__geo_interface__
#     print coords

# getting coordinates of a state
# for i in range(r.numRecords):
#     feature = r.shapeRecords()[i]
#     coords = feature.shape.__geo_interface__
#     print coords['coordinates'][0]
#     if type(coords['coordinates'][0]) != list:
#         #print coords['coordinates']
#         ls = list(coords['coordinates'][0])
#     else:
#         ls = coords['coordinates'][0]
#
#     print(ls[0])
#
#     poly = Polygon(ls)
#     #print poly
#     if test_coord.within(poly):
#         print("True")

# Given a latitude-longitude pair, find which polygon (state) contains it


# TEST:

# Create Point objects
p1 = Point(24.952242, 60.1696017)
p2 = Point(24.976567, 60.1612500)

# Create a Polygon
cords = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]
poly = Polygon(cords)

print p2.within(poly)

# point = Point(0.0, 0.0)
# print point.length

# from SO:


sf = shapefile.Reader("C:/Users/Shoto/PycharmProjects/LocalityTweets/venv/temp")
shapes = sf.shapes()
# shapes[i].points
fields = sf.fields
records = sf.records()
state_polygons = {}
for i, record in enumerate(records):
    state = record[5]
    points = shapes[i].points
    poly = Polygon(points)
    state_polygons[state] = poly

print state_polygons

# us border


# check if in one of the states then True, else False


def in_us(lat, lon):
    p = Point(lon, lat)
    for state, poly in state_polygons.iteritems():
        if poly.contains(p):
            return state
    return None

