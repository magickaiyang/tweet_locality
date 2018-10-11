import botometer

mashape_key = "kcjvCl6X8ymshjXv17CkMxGKR82tp1XzGQ9jsnYwTnGY6dgiye"
twitter_app_auth = {
    'consumer_key': 'M4RsO5BPSrhrqX4dTtVsjLKnF',
    'consumer_secret': 'tywdiv9Y4XimMzoJyeYJ85C3pKnRDXvlJpHt3nvEjgzqgEJv0P',
    'access_token': '1042434964334305281-BZRy2GIEUmYmyp4KVavu6YesSaMFe9',
    'access_token_secret': 'v4Z7x17IH7gOhIwgzbYSPgZO8J73EknuwlqqNFqZs01vo',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          mashape_key=mashape_key,
                          **twitter_app_auth)

# Check a single account by screen name
result = bom.check_account('@kamyavishwanath')

print result['display_scores']['english']
