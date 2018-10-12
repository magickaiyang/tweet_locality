from shapely.geometry import Point, Polygon
import shapefile

test_coord = Point(-86.990100, 40.332937)


def locate_country(lon, lat, country_fp):
    crf = shapefile.Reader(country_fp)
    shapes_countries = crf.shapes()
    country_polygons = {}
    # print(crf.records())
    for i, record in enumerate(crf.records()):
        country_polygons[record[3]] = Polygon(shapes_countries[i].points)

    pt = Point(lat, lon)
    this_country = ""
    for c, p in country_polygons.iteritems():
        # print p
        if p.contains(pt):
            this_country = c
            break

    return this_country


def locate_state(lon, lat, state_fp):
    sf = shapefile.Reader(state_fp)
    shapes_states = sf.shapes()
    state_polygons = {}
    for i, record in enumerate(sf.records()):
        state_polygons[record[5]] = Polygon(shapes_states[i].points)

    pt = Point(lat, lon)
    this_state = ""
    for s, p in state_polygons.iteritems():
        # print p
        if p.contains(pt):
            this_state = s
            break

    return this_state


def locate_county(lon, lat, county_fp):
    cf = shapefile.Reader(county_fp)
    shapes_counties = cf.shapes()
    county_polygons = {}
    # print(cf.records())
    for i, record in enumerate(cf.records()):
        county_polygons[record[5]] = Polygon(shapes_counties[i].points)

    pt = Point(lat, lon)
    this_county = ""

    for c, p in county_polygons.iteritems():
        # print(c)
        if p.contains(pt):
            this_county = c
            break

    return this_county


# print(locate_state(40.332937, -86.990100, 'venv/shapefiles/tl_2017_us_state/tl_2017_us_state'))

# print locate(40.332937, -86.990100, "venv/shapefiles/ne_110m_admin_0_countries/ne_110m_admin_0_countries",
# "venv/shapefiles/tl_2017_us_state/tl_2017_us_state", "venv/shapefiles/tl_2016_us_county/tl_2016_us_county")

