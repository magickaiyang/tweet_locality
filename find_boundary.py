from shapely.geometry import Point
import shapefile

myshp = open("C:/Users/Shoto/PycharmProjects/LocalityTweets/venv/shapefiles/tl_2017_us_state.shp", "rb")
mydbf = open("C:/Users/Shoto/PycharmProjects/LocalityTweets/venv/shapefiles/tl_2017_us_state.dbf", "rb")
r = shapefile.Reader(shp=myshp, dbf=mydbf)

# print r.numRecords

for i in range(r.numRecords):
    print r.record(i)

# point = Point(0.0, 0.0)
# print point.length

