SELECT users_2015_05_to_2017_12.user_id, us_blck_grp_2010.geoid10
	FROM users_2015_05_to_2017_12
	LEFT OUTER JOIN us_blck_grp_2010
	ON ST_Intersects(us_blck_grp_2010.geom, ST_Transform(ST_SetSRID(ST_MakePoint(users_2015_05_to_2017_12.home_lon, users_2015_05_to_2017_12.home_lat),4326), 4269))
	WHERE users_2015_05_to_2017_12.home_lon is not null
	LIMIT 100
	;