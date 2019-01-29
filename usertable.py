import csv
import pyodbc
import json

def add_tweets_number_toSQL():
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
    query = "SELECT [users] FROM [LOCALITY1].[dbo].[twitter_users]"
    cursor.execute(query)

    # Start with getting the first row
    row = cursor.fetchone()
    # row2 = cursor2.fetchone()

    # Initialize the json data(username as key, coordinates as value)
    data = {}
    data['users'] = []

    # Parsing each row
    while row:
        screenname = row[0]
        query2 = "Update [LOCALITY1].[dbo].[twitter_users] SET tweet_count = (SELECT COUNT(*) " \
                 "FROM [LOCALITY1].[dbo].[tweets] where screen_name = '" + screenname + "' )" +\
                 "WHERE users = '" + screenname + "'"
        cursor2.execute(query2)
        cnxn2.commit()

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