select countries.cntry_name, tweet.geo_lat, tweet.geo_long, tweet.tweet_text
	from world_countries_2017 as countries, tweet_us_2013_01_03 as tweet
	where ST_Intersects(countries.geom, ST_SetSRID(ST_MakePoint(tweet.geo_long, tweet.geo_lat),4326))
	limit 1000;
