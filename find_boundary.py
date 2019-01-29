from shapely.geometry import Point, Polygon
import shapefile


# Function to locate Country with latitude and longitude
# Argument as coordinates longitude, latitude, and file path of shapefile
# Return value as Country name
def locate_country(lon, lat, country_fp):
    # Read the shapefile
    crf = shapefile.Reader(country_fp)

    # Returns a list of Shape objects describing the geometry of
    # each shape record
    shapes_countries = crf.shapes()
    country_polygons = {}

    for i, record in enumerate(crf.records()):
        # The border is at the position of index 3
        country_polygons[record[1]] = Polygon(shapes_countries[i].points)

    # Make the lat and lon a Point object
    pt = Point(lon, lat)    # appears that longitude first, latitude second
    this_country = ""
    for c, p in country_polygons.iteritems():
        # Check if p contains the point
        if p.contains(pt):
            this_country = c
            break

    return this_country


# Function to locate State with latitude and longitude
# Argument as coordinates longitude, latitude, and file path of shapefile
# Return value as State name
def locate_state(lon, lat, state_fp):
    # Read the shapefile and store the
    sf = shapefile.Reader(state_fp)

    # Returns a list of Shape objects describing the geometry of
    # each shape record
    shapes_states = sf.shapes()
    state_polygons = {}

    for i, record in enumerate(sf.records()):
        # The boarder is at the position of index 5
        state_polygons[record[5]] = Polygon(shapes_states[i].points)

    # Make the lat and lon a Point object
    pt = Point(lat, lon)
    this_state = ""
    for s, p in state_polygons.iteritems():
        # Check if p contains the point
        if p.contains(pt):
            this_state = s
            break

    return this_state


# Function to locate County with latitude and longitude
# Argument as coordinates longitude, latitude, and file path of shapefile
# Return value as County name
def locate_county(lon, lat, county_fp):
    # Read the shapefile
    cf = shapefile.Reader(county_fp)

    # Returns a list of Shape objects describing the geometry of
    # each shape record
    shapes_counties = cf.shapes()

    county_polygons = {}
    # print(cf.records())
    for i, record in enumerate(cf.records()):
        # The boarder is at the position of index 5
        county_polygons[record[5]] = Polygon(shapes_counties[i].points)

    # Make the lat and lon a Point object
    pt = Point(lat, lon)
    this_county = ""

    for c, p in county_polygons.iteritems():
        # Check if p contains the point
        if p.contains(pt):
            this_county = c
            break

    return this_county


# Testing the above functions
# test_coord = Point(-86.990100, 40.332937)
# print(locate_state(45.016302, -79.609751, 'C:/_Study/crowdsourcing/tl_2017_us_state/tl_2017_us_state'))
# print locate(40.332937, -86.990100, "venv/shapefiles/ne_110m_admin_0_countries/ne_110m_admin_0_countries",
# "venv/shapefiles/tl_2017_us_state/tl_2017_us_state", "venv/shapefiles/tl_2016_us_county/tl_2016_us_county")

