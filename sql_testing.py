import csv
from itertools import islice
import pyodbc
import ast
import sys
from detect_bot import *
from dbscan_test import *
import re
from find_boundary import *


###
# Function to check if the time is between 8 pm to 5 am
# Takes string argument as time
# Returns false if it is not between the period
####
def check_time(time):
    times = re.split("\W", time)
    if times[3] <= "05" or times[3] >= "20":
        return True
    return False


####
# Function to read a specif data table and
# check created time if data is needed, store
# all coordinates for each user in a dictionary
# then save the data in an csv file(need to change)
# Takes the name of data table needs to be parsed

def build_usertable(data_table):
    # Specify config
    server = '128.46.137.201'
    database = 'LOCALITY1'
    username = 'localityedit'
    password = 'Edit123'
    # Connect to database
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()

    # Write query and execute
    query = "SELECT [screen_name],[created_at],[geo_lat],[geo_long] FROM " + data_table
    print query
    cursor.execute(query)

    # Start with getting the first row
    row = cursor.fetchone()
    print row

    # Initialize the cluster(username as key, coordinates array as value)
    clusters = {}

    current_row_index = 0
    # Parsing each row
    while row:
        username = row[0]
        created_time = str(row[1])
        coordinates = [row[2], row[3]]

        # Twitter message and bot detector are not needed temporarily
        # text = row[4]
        # if detectbot(username)<=2.5:

        # to find cluster for home location
        # if check_time(created_time):
        #     if username not in clusters.keys():
        #         clusters.update({username: {"coordinates": [coordinates], "home": []}})
        #     else:
        #         clusters[username]["coordinates"].append(coordinates)

        if check_time(created_time):
            if username not in clusters.keys():
                clusters.update({username: [coordinates]})
            else:
                clusters[username].append(coordinates)

        # cluster with text and coordinates, not needed temporarily
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

        if current_row_index % 1000 == 0:
            print 'Current row ' + current_row_index    # occasional print
        row = cursor.fetchone()
        current_row_index += 1


    cursor = cnxn.cursor()

    for username in clusters.keys():
        if len(clusters[username]) >= 3:
            execute_line = "INSERT INTO [LOCALITY1].[localityedit].[user_coordinates_2] (users, coordinates) VALUES ('" + str(username)\
                           + "', '" + str(clusters[username]) + "')"
            print(execute_line)
            cursor.execute(execute_line)
            cnxn.commit()
    # Write to csv file (need to change to other methods)
    # with open('users.csv', 'wb') as csv_file:
    #     writer = csv.writer(csv_file)
    #     for key, value in clusters.items():
    #         writer.writerow([key, value])
    #
    # return "csv file is complete"

    # Previous tries
    # cursor = cnxn.cursor()
    # for username in clusters.keys():
    #     if len(clusters[username]["coordinates"]) > 20:
    #         try:
    #             center = get_center_in_cluster(clusters[username]["coordinates"])
    #         except:
    #             print(clusters[username])
    #             with open('errors.csv', 'wb') as csv_file:
    #                 writer = csv.writer(csv_file)
    #                 for key, value in clusters.items():
    #                     writer.writerow([key, value])
    #             continue
    #         clusters[username]["home"] = center
    #         # DO THIS FIRST
    #         execute_line = "INSERT INTO [LOCALITY1].[dbo].[updated_users] (screenname, lat, lon) VALUES ('" + username + "', '" + str(
    #             clusters[username]["home"][0]) + "', '" + str(clusters[username]["home"][1]) + "')"
    #         # print(execute_line)
    #         cursor.execute(execute_line)
    #         cnxn.commit()


    # cursor = cnxn.cursor()
    # cursor1 = cnxn.cursor()
    # cursor.execute("SELECT [screenname] FROM [LOCALITY1].[dbo].[twitter_users]")
    # row = cursor.fetchone()
    # bot_score = 0
    # while row:
    #     # bot_score = detectbot(row)
    #     execute_line = "INSERT INTO [LOCALITY1].[dbo].[twitter_users] (bot_score) VALUES ('" + str(bot_score) + "')"
    #     # cursor1.execute(execute_line)
    #     cnxn.commit()
    #     row = cursor.fetchone()


####
# Useless tries to deduct duplicate home locations,
# should be ignored
###########
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


def construct_coordinates(coor_str):
    coordinates=ast.literal_eval(coor_str)
    return coordinates

####
# Failed function to read from existing user table csv file
# and upload data into sql database
# Should not use it anymore
#####
def read_to_user_table(filename):
    server = '128.46.137.201'
    database = 'LOCALITY1'
    username = 'localityedit'
    password = 'Edit123'
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    maxInt = sys.maxsize
    decrement = True
    while decrement:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.

        decrement = False
        try:
            csv.field_size_limit(maxInt)
        except OverflowError:
            maxInt = int(maxInt / 10)
            decrement = True
    print "resized"
    counter = 0
    with open(filename, "rb") as f:
        reader = csv.reader(f, delimiter=",")
        for row in islice(reader, 10723, None):
        # for row in reader:
            if counter > 5562:
                print counter
            counter += 1
            screenname = row[0]
            centers = ast.literal_eval(row[1])["coordinates"]
            # print type(centers["coordinates"])
            if len(centers) > 20:
                # The program will fail after reading a certain number
                # of data, so we tried to stored the errors in another
                # file. Still wrong method
                try:
                    center = get_center_in_cluster(centers)
                except:
                    print row
                    with open('errors.csv', 'wb') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow([row[0], row[1]])
                    continue
                execute_line = "INSERT INTO [LOCALITY1].[dbo].[updated_users] (screenname, lat, lon) VALUES ('" + screenname + "', '" + str(
                    center[0]) + "', '" + str(center[1]) + "')"
                cursor.execute(execute_line)
                cnxn.commit()

###########
# Function to store home location into user table
###########
def get_home_usertable(data_table):
    # Specify config
    server = '128.46.137.201'
    database = 'LOCALITY1'
    username = 'localityedit'
    password = 'Edit123'
    # Connect to database
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()

    # Write query and execute
    query = "SELECT [users],[coordinates] FROM " + data_table
    print query
    cursor.execute(query)

    # Start with getting the first row
    row = cursor.fetchone()
    print row

    # Initialize the cluster(username as key, coordinates array as value)
    usertable = {}

    # Parsing each row
    while row:
        username = row[0]
        coordinates = construct_coordinates(row[1])

        home = get_center_in_cluster(coordinates)
        if home != None:
            usertable.update({username: home})

        row = cursor.fetchone()

    cursor = cnxn.cursor()

    for username in usertable.keys():
        execute_line = "INSERT INTO [LOCALITY1].[localityedit].[user_table] (users, home_lat, home_lon) VALUES ('" + str(username)\
                           + "', '" + str(usertable[username][0]) + "', '" + str(usertable[username][1]) + "')"
        print(execute_line)
        cursor.execute(execute_line)
        cnxn.commit()


# Code to run and test the above functions.

# clusters = {'screenname':[[40.430023, -86.909103], [40.422363, -86.876788], [40.422363, -86.876683],
#                                [40.425368, -86.895309], [40.366318, -86.752251]],
#             'hello': [[40.430023, -86.909123], [40.422343, -86.876788], [40.422863, -86.876683]]}
#
# with open('dict.csv', 'wb') as csv_file:
#     writer = csv.writer(csv_file)
#     for key, value in clusters.items():
#         writer.writerow([key, value])

# with open('dict.csv', 'rb') as csv_file:
#     reader = csv.reader(csv_file)
#     mydict = dict(reader)
# print("dictionary type:" + str(mydict))


# print(build_usertable("[LOCALITY1].[dbo].[tweets]"))

# read_to_user_table("users.csv")


build_usertable("[LOCALITY1].[dbo].[tweets]")
#print(type(construct_coordinates('[[28.39499,-83,4900],[23.492,-32.1111]]')[0][0]))
