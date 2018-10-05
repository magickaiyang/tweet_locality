from shapely.geometry import Point, Polygon
import shapefile


test_coord = Point(-86.990100, 40.332937)

sf = shapefile.Reader("C:/Users/Shoto/PycharmProjects/LocalityTweets/venv/shapefiles/tl_2017_us_state/tl_2017_us_state")
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


def in_us(lat, lon):
    pt = Point(lat, lon)
    for s, p in state_polygons.iteritems():
        if p.contains(pt):
            return s
    return "not found"


print in_us(-86.990100, 40.332937)
