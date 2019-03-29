update us_blck_grp_2010 set user_count_2014_2015 =
	(
	select count(user_id) from users_2014_10_to_2015_04
		where users_2014_10_to_2015_04.home_block_group = us_blck_grp_2010.geoid10
	);