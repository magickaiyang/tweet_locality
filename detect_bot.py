import botometer


# Function to check the possibility if the user is a bot
# Argument username is the screenname of tweeter user
# Return value is the possibility, 0 as lowest, 5 as highest possibility
# Note: if the user canceled the account, the return value will be 5
def detectbot(username):

    # Authorization token for the Botometer
    mashape_key = "kcjvCl6X8ymshjXv17CkMxGKR82tp1XzGQ9jsnYwTnGY6dgiye"

    # Authorization token for the Twitter
    twitter_app_auth = {
        'consumer_key': 'M4RsO5BPSrhrqX4dTtVsjLKnF',
        'consumer_secret': 'tywdiv9Y4XimMzoJyeYJ85C3pKnRDXvlJpHt3nvEjgzqgEJv0P',
        'access_token': '1042434964334305281-BZRy2GIEUmYmyp4KVavu6YesSaMFe9',
        'access_token_secret': 'v4Z7x17IH7gOhIwgzbYSPgZO8J73EknuwlqqNFqZs01vo',
    }

    # Get the score
    bom = botometer.Botometer(wait_on_ratelimit=True,
                          mashape_key=mashape_key,
                          **twitter_app_auth)

    # Check a single account by screen name
    try:
        result = bom.check_account(username)
        # return the possibility of being a bot
        return result['display_scores']['universal']

    except:
        # if error occurs, return 5
        return 5
