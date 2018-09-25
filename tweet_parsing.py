import tweepy
from parse_json import read_line


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)


def main():
    consumer_token = "M4RsO5BPSrhrqX4dTtVsjLKnF"
    consumer_secret = "tywdiv9Y4XimMzoJyeYJ85C3pKnRDXvlJpHt3nvEjgzqgEJv0P"

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(consumer_token, consumer_secret)

    api = tweepy.API(auth)

    print("please visit: %s" % auth.get_authorization_url())
    verifier = input("after you grant access what is the verifier code? ")
    auth.get_access_token(verifier)
    public_tweets = api.home_timeline()

    output_file = open("tweet_output.txt", "w")

    for tweet in public_tweets:
        print(tweet.text)
        output_file.write(tweet.text)
        output_file.write(read_line(tweet.text))

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    LOCATION = [5.0770049095, 47.2982950435, 15.0403900146, 54.9039819757]
    # LOCATION = [-88.099701, 37.771744, -84.784607, 37.771744]
    myStream.filter(locations=LOCATION)


main()
