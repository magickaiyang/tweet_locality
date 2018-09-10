import json

with open ('test.json') as f:
    data = json.load(f)

for feature in data ['features']:
    print "type is " + feature['geometry']['type']
    print "coordinates are " + str(feature['geometry']['coordinates'])
    print "alternate names are " + str(feature['properties']['alternateNames'])
    print "positions are " + str(feature['properties']['positions'])
