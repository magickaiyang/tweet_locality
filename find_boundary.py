from shapely.geometry import Point, Polygon
import shapefile

test_coord = Point(-86.990100, 40.332937)


def locate(lon, lat, country_fp, state_fp, county_fp):
    sf = shapefile.Reader(state_fp)
    crf = shapefile.Reader(country_fp)
    cf = shapefile.Reader(county_fp)

    # sf = shapefile.Reader("venv/shapefiles/tl_2017_us_state/tl_2017_us_state")
    # cf = shapefile.Reader("venv/shapefiles/TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS-0.3")
    # cf = shapefile.Reader("venv/shapefiles/tl_2016_us_county/tl_2016_us_county")

    shapes_states = sf.shapes()
    state_polygons = {}
    for i, record in enumerate(sf.records()):
        state_polygons[record[5]] = Polygon(shapes_states[i].points)

    shapes_counties = cf.shapes()
    county_polygons = {}
    # print(cf.records())
    for i, record in enumerate(cf.records()):
        county_polygons[record[5]] = Polygon(shapes_counties[i].points)
        # print county_polygons[record[5]]
    # print(county_polygons['Tippecanoe County'])

    shapes_countries = crf.shapes()
    country_polygons = {}
    # print(crf.records())
    for i, record in enumerate(crf.records()):
        country_polygons[record[3]] = Polygon(shapes_countries[i].points)

    # print(country_polygons[0])

    this_county = ""
    this_country = ""
    this_state = ""
    pt = Point(lat, lon)

    for s, p in state_polygons.iteritems():
        #print p
        if p.contains(pt):
            this_state = s
            break

    for c, p in county_polygons.iteritems():
        # print(c)
        if p.contains(pt):
            this_county = c
            break

    for c, p in country_polygons.iteritems():
        # print p
        if p.contains(pt):
            this_country = c
            break

    return this_county + " " + this_state + " " + this_country


print locate(40.332937, -86.990100, "venv/shapefiles/ne_110m_admin_0_countries/ne_110m_admin_0_countries", "venv/shapefiles/tl_2017_us_state/tl_2017_us_state", "venv/shapefiles/tl_2016_us_county/tl_2016_us_county")

