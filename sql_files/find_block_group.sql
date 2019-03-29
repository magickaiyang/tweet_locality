UPDATE users_2014_10_to_2015_04 SET home_block_group =
(
	SELECT us_blck_grp_2010.geoid10 FROM us_blck_grp_2010
		WHERE ST_Within(ST_Transform(ST_SetSRID(ST_MakePoint(users_2014_10_to_2015_04.home_lon, users_2014_10_to_2015_04.home_lat),4326), 102003), us_blck_grp_2010.geom)
		LIMIT 1
)