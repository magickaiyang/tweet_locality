from tweet_locations import *
from detect_bot import *
import tweepy

# Maximum number of tweets that can be parsed
MAX_TWEETS = 5

texts = []
locations = []


# Class and functions to create the tweeter steamer,
# used to achieve tweeter streaming
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super(MyStreamListener, self).__init__(api)
        self.num_tweets = 0

    def on_status(self, status):
        # if number of tweets exceeds the Maximum, end the streaming
        if self.num_tweets >= MAX_TWEETS:
            return False

        location = str([])
        username = status.user.screen_name

        # Calling botometer to determine if the user is a bot
        score = detectbot(username)
        print(username + " - score is "+str(score))
        if score < 2.5:
            if status.place:
                # Analyzing the tweeter object using geoText
                location = str(status.place.bounding_box.coordinates)
                #print(location)

            print(tweet_country(status))
            text = status.text
            texts.append(text)
            print(status.text)
            locations.append(location)
            self.num_tweets += 1


def main():
    # Authorization of Tweepy
    consumer_token = "M4RsO5BPSrhrqX4dTtVsjLKnF"
    consumer_secret = "tywdiv9Y4XimMzoJyeYJ85C3pKnRDXvlJpHt3nvEjgzqgEJv0P"
    access_token = "1042434964334305281-BZRy2GIEUmYmyp4KVavu6YesSaMFe9"
    access_secret = "v4Z7x17IH7gOhIwgzbYSPgZO8J73EknuwlqqNFqZs01vo"

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    # Create the Steamer using the class initialized above
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    # The Location states the boundary of the tweets
    # [longitude1, latitude1, longitude2, latitude2]
    LOCATION = [-86.990100, 40.332937, -86.765386, 40.474450]

    # two longitude/latitude pairs, with the first pair denoting the southwest corner of the box
    # west lafayette and lafayette [-86.990100, 40.332937, -86.765386, 40.474450]
    myStream.filter(locations=LOCATION)


main()


