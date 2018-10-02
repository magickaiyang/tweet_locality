import parser
import tweepy


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        location = status.coordinates.coordinates
        text = status.text
        print(str(status.user.name)+": "+str(status.text))


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

