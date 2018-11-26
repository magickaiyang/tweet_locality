import pyodbc
from detect_bot import *
from dbscan_test import *
import re
from find_boundary import *

def check_time(time):
    times = re.split("\W", time)
    if times[3]<="04" or times[3]>="20":
        return True
    return False

def build_usertable(data_table):
    server = '128.46.137.201'
    database = 'LOCALITY1'
    username = 'localityedit'
    password = 'Edit123'
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()

    query = "SELECT [screen_name],[created_at],[geo_lat],[geo_long] FROM " + data_table
    cursor.execute(query)
    row = cursor.fetchone()

    dicti = {}
    clusters = {}

    while row:
        username = row[0]
        created_time = str(row[1])
        coordinates = [row[2], row[3]]
        # text = row[4]
        # if detectbot(username)<=2.5:

        # to find cluster for home location
        if check_time(created_time):
            if username not in clusters.keys():
                clusters.update({username: {"coordinates": [coordinates], "home": []}})
            else:
                clusters[username]["coordinates"].append(coordinates)

        # cluster with text and coordinates
        # if username not in dicti.keys():
        #     if check_time(created_time):
        #         dicti.update({username: {"coordinates": [coordinates], "text": [text], "home": []}})
        #     else:
        #         dicti.update({username: {"coordinates": [], "text": [text], "home": []}})
        # else:
        #     if check_time(created_time):
        #         dicti[username]["coordinates"].append(coordinates)
        #         dicti[username]["text"].append(text)
        #     else:
        #         dicti[username]["text"].append(text)

        row = cursor.fetchone()

    print(clusters)
    cursor = cnxn.cursor()
    for username in clusters.keys():
        if len(clusters[username]["coordinates"]) > 20:
            center = get_center_in_cluster(clusters[username]["coordinates"])
            clusters[username]["home"] = center
            # DO THIS FIRST
            execute_line = "INSERT INTO [LOCALITY1].[dbo].[twitter_users] (screenname, lat, lon) VALUES ('" + username + "', '" + str(
                clusters[username]["home"][0]) + "', '" + str(clusters[username]["home"][1]) + "')"
            # print(execute_line)
            cursor.execute(execute_line)
            cnxn.commit()


def deduct_home_location():
    server = '128.46.137.201'
    database = 'LOCALITY1'
    username = 'localityedit'
    password = 'Edit123'
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    query = "SELECT [screenname],[lat],[lon] FROM [LOCALITY1].[dbo].[twitter_users]"
    cursor.execute(query)
    row = cursor.fetchone()

    user_homes = {}
    while row:
        name = row[0]
        home = [row[1], row[2]]
        if name not in user_homes.keys():
            user_homes.update({name:[home]})
        else:
            user_homes[name].append(home)

        row = cursor.fetchone()

    print()
    user_homes_updated = {}
    for user in user_homes.keys():
        print(user + " home:" + str(user_homes[user]))
        center = user_homes[user][0]
        if len(user_homes[user]) > 2:
            center = get_center_in_cluster(user_homes[user])
        if len(user_homes[user]) == 2:
            first_state = locate_state(user_homes[user][0][0],user_homes[user][0][1], 'C:/_Study/crowdsourcing/tl_2017_us_state/tl_2017_us_state')
            second_state = locate_state(user_homes[user][1][0], user_homes[user][1][1],
                                       'C:/_Study/crowdsourcing/tl_2017_us_state/tl_2017_us_state')
            if first_state == "" and second_state == "":
                continue
            if first_state != second_state:
                print("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO!")
                print(first_state + " and " + second_state)
                continue

        if user not in user_homes_updated.keys():
            user_homes_updated.update({user: [center]})

        else:
            print("Not possible!")


deduct_home_location()



