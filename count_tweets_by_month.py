import pyodbc
import datetime


def connect_database(server, username, password, database, driver):
    cnxn = pyodbc.connect(
        'DRIVER={' + driver + '};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return cnxn


def count_tweets_by_month():
    cnxn = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode')

    for i in range(2013, 2019):
        for j in range(1, 13):
            # stops at 2018-09
            if i == 2018 and j >= 10:
                break

            table = 'tweet_us_' + str(i) + '_'
            if 3 >= j >= 1:
                table = table + '01_03'
            elif 6 >= j >= 4:
                table = table + '04_06'
            elif 9 >= j >= 7:
                table = table + '07_09'
            elif 12 >= j >= 10:
                table = table + '10_12'

            this_month = datetime.datetime(year=i, month=j, day=1)
            if j == 12:
                next_month = datetime.datetime(year=i + 1, month=1, day=1)
            else:
                next_month = datetime.datetime(year=i, month=j + 1, day=1)

            query = "SELECT count(*) FROM " + table + ' WHERE created_at>=\'' \
                    + this_month.strftime('%Y-%m-%d') + '\' AND created_at<\'' + next_month.strftime('%Y-%m-%d') + '\''
            cursor = cnxn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()

            print('{}\t{}'.format(this_month.strftime('%Y-%m'), row[0]))


count_tweets_by_month()
