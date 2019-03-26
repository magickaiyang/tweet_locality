SELECT tweets.user_id, tweets.tweet_id, tweets.created_at, tweets.geo_lat, tweets.geo_long, tweets.tweet_text, tweets.source, world_countries_2017.cntry_name
	FROM tweets
	LEFT OUTER JOIN world_countries_2017
	ON ST_Intersects(world_countries_2017.geom, ST_SetSRID(ST_MakePoint(tweets.geo_long, tweets.geo_lat),4326))
	;