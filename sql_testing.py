import pyodbc
from detect_bot import *
from dbscan_test import *
import re

def check_time(time):
    times = re.split("\W", time)
    if times[3]<="04" or times[3]>="17":
        return True
    return False

server = '128.46.137.201'
database = 'LOCALITY1'
username = 'localityedit'
password = 'Edit123'
cnxn = pyodbc.connect(
    'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()

cursor.execute("SELECT [screen_name],[created_at],[geo_lat],[geo_long] FROM [LOCALITY1].[dbo].[tweet_us_2016_01]")
row = cursor.fetchone()

dicti = {}
clusters = {}
c = 0
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
        print clusters[username]["home"]
        # DO THIS FIRST
        execute_line = "INSERT INTO [LOCALITY1].[dbo].[twitter_users] (screenname, lat, lon) VALUES ('" + username + "', '" + str(
            clusters[username]["home"][0]) + "', '" + str(clusters[username]["home"][1]) + "')"
        # print(execute_line)
        cursor.execute(execute_line)
        cnxn.commit()



