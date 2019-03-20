CREATE TABLE tweets_2014_10_to_2015_04
	AS(
		SELECT user_id, tweet_id, created_at, geo_lat, geo_long, tweet_text FROM tweet_us_2014_10_12
		UNION ALL
		SELECT user_id, tweet_id, created_at, geo_lat, geo_long, tweet_text FROM tweet_us_2015_01_03
		UNION ALL
		(
			SELECT user_id, tweet_id, created_at, geo_lat, geo_long, tweet_text FROM tweet_us_2015_04_06
			where created_at >= '2015-04-01'
				and created_at < '2015-05-01'
		)
	);