import pyodbc
import holidays
import collections
from dbscan_test import get_center_in_cluster


# Function to connect to database, return cnxn
def connect_database(server, username, password, database, driver):
    cnxn = pyodbc.connect(
        'DRIVER={' + driver + '};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return cnxn


def check_time(time):
    # times = re.split("\W", str(time))    # split time string with regular expression, condition: non alphanumeric
    # year = int(times[0])
    # month = int(times[1])
    # date = int(times[2])

    if time.hour <= 23 and time.hour >= 20:
        day = time.weekday()
        if 4 >= day >= 1:
            if time not in holidays.US():
                return True
    return False


def add_home_coor(tweet_table, user_table):
    user_cnxn = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')
    user_cursor = user_cnxn.cursor()

    tweets_cnxn = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')
    tweets_cursor = tweets_cnxn.cursor()

    insert_cnxn = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')
    insert_cursor = insert_cnxn.cursor()

    user_query = "SELECT user_id FROM " + user_table + ' ORDER BY user_id ASC'
    user_cursor.execute(user_query)

    # Start with getting the first row
    row = user_cursor.fetchone()

    # Parsing each row
    while row:
        print("User id: " + str(row[0]))
        coords = []
        date_times = []
        texts = []

        user_id = row[0]
        tweets_query = "SELECT created_at, geo_lat, geo_long, tweet_text FROM " + tweet_table + \
                       " WHERE user_id = " + str(user_id) + ' ORDER BY created_at ASC'
        tweets_cursor.execute(tweets_query)
        tweet = tweets_cursor.fetchone()

        while tweet:
            texts.append(tweet[3])
            if check_time(tweet[0]):
                coords.append([tweet[1], tweet[2]])
                date_times.append(tweet[0])

            tweet = tweets_cursor.fetchone()

        # check if it contains more than 10% duplicate
        counter = collections.Counter(texts)
        total_count = 0
        for c in counter.values():
            if c > 1:
                total_count += c
        if total_count < 0.1 * sum(counter.values()):

            if len(coords) >= 3:
                home = get_center_in_cluster(coords, user_id, tweet_table)

                if home is not None:
                    insert_query = "UPDATE " + user_table + " SET home_lat = '" + str(home[0]) + \
                                   "', home_lon = '" + str(home[1]) + "' WHERE user_id = " + str(user_id)
                    insert_cursor.execute(insert_query)
                    insert_cnxn.commit()

        row = user_cursor.fetchone()


def add_home_country_toSQL(user_table, shapefile_path):
    # Connect to database
    cnxn = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')
    cnxn2 = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')

    cursor = cnxn.cursor()
    cursor2 = cnxn2.cursor()

    # Write query and execute
    query = "SELECT [user_id], [home_lat], [home_lon] FROM" + user_table
    cursor.execute(query)

    # Start with getting the first row
    row = cursor.fetchone()

    # Parsing each row
    while row:
        user_id = row[0]
        lat = row[1]
        lon = row[2]

        country = locate_country(lat, lon, shapefile_path)
        query2 = "Update " + user_table + " SET home_country = '" + country + "' WHERE user_id = " + user_id
        cursor2.execute(query2)
        cnxn2.commit()

        row = cursor.fetchone()


####
# get percentage of tweets with place/ total number of tweets
#######
def tweets_percentage_of_place_in_usertable(user_table, tweet_table):
    cnxn = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')
    cnxn2 = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')
    cnxn3 = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')

    cursor = cnxn.cursor()
    cursor2 = cnxn2.cursor()
    cursor3 = cnxn3.cursor()

    # Write query and execute
    query = "SELECT [users],[tweet_count] FROM " + str(user_table)
    cursor.execute(query)

    # Start with getting the first row
    row = cursor.fetchone()

    while row:
        user_id = row[0]
        tweets_count = row[1]
        place_count = 0
        query2 = "SELECT * FROM " + str(tweet_table) + " where user_id = '" + user_id + "'"
        cursor2.execute(query2)
        row2 = cursor2.fetchone()
        while row2:
            tweet_text = row2[4]
            if parse_text(tweet_text, "") is not None:
                place_count += 1

        percentage = float(place_count) / tweets_count
        query3 = "UPDATE " + str(user_table) + " SET percent_place = " + str(
            percentage) + " WHERE user_id = '" + user_id + "'"
        cursor3.execute(query3)
        row = cursor.fetchone()


def place_count_in_tweets(tweet_table):
    cnxn = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')
    cnxn2 = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')

    cursor = cnxn.cursor()
    cursor2 = cnxn2.cursor()

    query = "SELECT [tweet_text], [tweet_id] FROM " + str(tweet_table)

    cursor.execute(query)
    row = cursor.fetchone()

    while row:
        tweet_text = row[0]
        id = row[1]
        geojson_data = parse_text(tweet_text, "")
        place_count = 0
        if geojson_data is not None:
            place_count = len(geojson_data['features'])

        query2 = "UPDATE " + tweet_table + " SET place_count = " + str(place_count) + " WHERE tweet_id = " + str(id)
        cursor2.execute(query2)
        cnxn2.commit()

        row = cursor.fetchone()


def percentage_about_home_country(user_table, tweet_table):
    cnxn = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')
    cnxn2 = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')
    cnxn3 = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')

    cursor = cnxn.cursor()
    cursor2 = cnxn2.cursor()
    cursor3 = cnxn3.cursor()

    # Write query and execute
    query = "SELECT [user_id],[tweet_count],[home_country] FROM " + user_table
    cursor.execute(query)

    # Start with getting the first row
    row = cursor.fetchone()

    while row:
        user_id = row[0]
        tweets_count = row[1]
        home_country = row[2]
        place_count = 0
        query2 = "SELECT * FROM " + tweet_table + " where user_id = '" + user_id + "'"
        cursor2.execute(query2)
        row2 = cursor2.fetchone()
        while row2:
            tweet_text = row2[4]
            data = parse_text(tweet_text, "")
            if data is not None:
                countries = get_country_code(data)
                if home_country not in countries or len(countries) > 1:
                    place_count += 1

        percentage = float(place_count) / tweets_count
        query3 = "UPDATE " + user_table + " SET about_home = " + str(percentage) + " WHERE user_id = '" + user_id + "'"
        cursor3.execute(query3)
        row = cursor.fetchone()


def usertable_to_csv(data_table):
    # Specify config
    server = '128.46.137.201'
    database = 'LOCALITY1'
    username = 'localityedit'
    password = 'Edit123'
    # Connect to database
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cnxn2 = pyodbc.connect(
        'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    cursor2 = cnxn2.cursor()

    # Write query and execute
    query = "SELECT [users],[home_lat], [home_lon] FROM " + data_table
    cursor.execute(query)

    # Start with getting the first row
    row = cursor.fetchone()
    # row2 = cursor2.fetchone()

    # Initialize the json data(username as key, coordinates as value)
    data = {}
    data['users'] = []

    # Parsing each row
    with open('usertable.csv', 'w') as f:
        while row:
            screenname = row[0]
            lat = row[1]
            lon = row[2]

            num_tweets_query = "SELECT COUNT(*) FROM [LOCALITY1].[dbo].[tweets] where screen_name = '" + screenname + "'"
            cursor2.execute(num_tweets_query)
            row2 = cursor2.fetchone()
            num_tweets = row2[0]

            writer = csv.writer(f, lineterminator='\n', delimiter=',')
            writer.writerow([float(lat), float(lon), num_tweets])
            row = cursor.fetchone()


add_home_coor("tweets_2014_10_to_2015_04", "users_2014_10_to_2015_04")

# add_home_coor("tweets_2015_05_to_2017_12", "users_2015_05_to_2017_12")
