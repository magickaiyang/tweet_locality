from parse_Geotxt import *
from find_boundary import *


def tweet_country(tweet):
    #if tweet.coordinates:
    if tweet.place:
        #real_coor = tweet.coordinates.coordinates
        real_coor = tweet.place.bounding_box.coordinates[0][0]
        print(real_coor)
        country = locate_country(real_coor[0], real_coor[1], 'C:/Users/Shoto/PycharmProjects/ne_110m_admin_0_countries/ne_110m_admin_0_countries')
        toponym = get_toponym(parse_text(tweet.text,2))
        counter = 0
        if len(toponym) == 0:
            return "No place in tweet text"

        for t in toponym:
            if t.contains(country):
                counter += 1

        if counter < len(toponym):
            return "Global"
        else:
            return "Domestic"
