import json

import requests
import tweepy

from detect_bot import *

MAX_TWEETS = 5
M_PARAMETER = 'm=gates&q='
output_file = open("tweet_output.txt", "w")
location_file = open("location_output.txt", "w")
texts = []
locations = []


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super(MyStreamListener, self).__init__(api)
        self.num_tweets = 0

    def on_status(self, status):
        if self.num_tweets >= MAX_TWEETS:
            return False

        location = str([])

        username = status.user.screen_name
        score = detectbot(username)
        print(username + " - score is "+str(score))
        if score < 2.5:
            if status.place:
                location = str(status.place.bounding_box.coordinates)
                print(location)

            text = status.text
            texts.append(text)
            print(status.text)
            locations.append(location)
            self.num_tweets += 1

def read_line(line):
    request_line = 'http://geotxt.org/v2/api/geotxt.json?' + M_PARAMETER + line
    #print(request_line)
    r = requests.get(request_line)
    data = r.json()

    toponyms = get_toponym(data)
    locations = get_location(data)

    result = ""
    for i in range(0, len(toponyms)):
        result += (str(i) + ": \n" + toponyms[i] + "\n" + str(locations[i]) + "\n\n")

    if result=="":
        result = "No Location in the text"
    return result


def get_toponym(data):
    result = []
    for places in data['features']:
        toponym = places['properties']['toponym']
        for hierarchy in places['properties']['hierarchy']['features']:
            toponym = toponym + ", " + hierarchy['properties']['toponym']
        result.append(toponym)
    return result


def get_location(data):
    result = []
    for places in data['features']:
        result.append(json.dumps(places['geometry']))
    return result


def main():
    consumer_token = "M4RsO5BPSrhrqX4dTtVsjLKnF"
    consumer_secret = "tywdiv9Y4XimMzoJyeYJ85C3pKnRDXvlJpHt3nvEjgzqgEJv0P"
    access_token = "1042434964334305281-BZRy2GIEUmYmyp4KVavu6YesSaMFe9"
    access_secret = "v4Z7x17IH7gOhIwgzbYSPgZO8J73EknuwlqqNFqZs01vo"

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    LOCATION = [-86.990100, 40.332937, -86.765386, 40.474450]
    # two longitude/latitude pairs, with the first pair denoting the southwest corner of the box
    # west lafayette and lafayette [-86.990100, 40.332937, -86.765386, 40.474450]
    myStream.filter(locations=LOCATION)



main()

for text in texts:
    output_file.write(read_line(text))
for location in locations:
    location_file.write(location+"\n")

output_file.close()
location_file.close()

