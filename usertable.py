import csv
import pyodbc
import json
import re
import pandas as pd
import holidays
import datetime

from datetime import datetime
from dbscan_test import get_center_in_cluster
from find_boundary import *
from parse_Geotxt import *
# from stdbscan import *


#############
# Function to get week day by from input of year, month, date
# return 0 as Sunday, 1 Monday, etc
#############
def getDay(year, month, date):
    if month == 1 or month == 2:
        year -= 1
    D = year%100
    C = year/100
    day = (date + ((13 * ((month+21)%12 + 1) - 1)/5) + D + D/4 + C/4 - 2 * C) % 7
    return day


# Function to connect to database, return cnxn
def connect_database(server, username, password, database, driver):
    cnxn = pyodbc.connect(
        'DRIVER={' + driver + '};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return cnxn


def check_time(time):
    times = re.split("\W", time)    # split time string with regular expression, condition: non alphanumeric
    year = int(times[0])
    month = int(times[1])
    date = int(times[2])



    if times[3] <= "05" or times[3] >= "20":
        day = getDay(year, month, date)
        if day <= 4 and day >= 1:
            if datetime.date(year, month, date) not in holidays.US():
                return True
    return False


def add_home_coor(tweet_table, user_table):
    user_cnxn = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')
    user_cursor = user_cnxn.cursor()

    tweets_cnxn = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')
    tweets_cursor = tweets_cnxn.cursor()

    insert_cnxn = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')
    insert_cursor = insert_cnxn.cursor()

    user_query = "SELECT user_id FROM " + user_table
    user_cursor.execute(user_query)

    # Start with getting the first row
    row = user_cursor.fetchone()

    # Parsing each row
    while row:
        coords = []
        lats = []
        lons = []
        date_times = []

        user_id = row[0]
        tweets_query = "SELECT created_at, geo_lat, geo_long from " + tweet_table + " WHERE user_id = " + str(user_id)
        tweets_cursor.execute(tweets_query)
        tweet = tweets_cursor.fetchone()

        while tweet:
            date_times.append(tweet[0])
            lats.append(tweet[1])
            lons.append(tweet[2])
            tweet = tweets_cursor.fetchone()

            if check_time(tweet[0]):
                coords.append([tweet[1], tweet[2]])
                tweet = tweets_cursor.fetchone()

        # data = {'latitude': lats, 'longitude': lons, 'date_time': date_times}
        # df = pd.DataFrame(data)
        # print(df)
        # st_dbscan = STDBSCAN(col_lat='latitude', col_lon='longitude',
        #                      col_time='date_time', spatial_threshold=500,
        #                      temporal_threshold=600, min_neighbors=5)
        #
        # result_t600 = st_dbscan.run(df)
        #
        # # -1 in cluster column denotes noise
        # print(result_t600)

        home = get_center_in_cluster(coords, user_id, tweet_table)
        if home is not None:

            insert_query = "Update " + user_table + " SET home_lat = '" + str(home[0]) + "', home_lon = '" + str(home[1]) + "' WHERE user_id = " + str(user_id)
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


def add_tweets_number_toSQL(user_table, tweet_table):
    user_cnxn = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')
    tweet_cnxn = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')
    user_cursor = user_cnxn.cursor()
    tweet_cursor = tweet_cnxn.cursor()

    # Write query and execute
    user_query = "SELECT [user_id] FROM " + str(user_table)
    user_cursor.execute(user_query)

    # Start with getting the first row
    row = user_cursor.fetchone()

    # Parsing each row
    while row:
        user_id = row[0]
        insert_query = "Update " + str(user_table) + " SET tweet_count = (SELECT COUNT(*) " \
                 "FROM " + str(tweet_table) + " where user_id = '" + user_id + "' )" +\
                 "WHERE user_id = '" + user_id + "'"
        tweet_cursor.execute(insert_query)
        tweet_cnxn.commit()

        row = user_cursor.fetchone()


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

        percentage = float(place_count)/tweets_count
        query3 = "UPDATE " + str(user_table) + " SET percent_place = " + str(percentage) + " WHERE user_id = '" + user_id + "'"
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
        user_id  = row[0]
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

        percentage = float(place_count)/tweets_count
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

# usertable_to_csv("[LOCALITY1].[dbo].[twitter_users]")
add_tweets_number_toSQL()