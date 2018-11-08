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

cursor.execute("SELECT [created_at],[screen_name],[geo_lat],[geo_long],[tweet_text], [source] FROM [LOCALITY1].[dbo].[tweet_us_2016_01_03]")
row = cursor.fetchone()

dicti = {}
c = 0
while row:
    created_time = row[0]
    username = row[1]
    coordinates = [row[2], row[3]]
    text = row[4]
    source = row[5]
    # if detectbot(username)<=2.5:

    if username not in dicti.keys():
        if ("Instagram" in source or "iPhone" in source or "Android" in source) and check_time(created_time):
            dicti.update({username: {"coordinates": [coordinates], "text": [text], "home": []}})
        else:
            dicti.update({username: {"coordinates": [], "text": [text], "home": []}})
    else:
        if ("Instagram" in source or "iPhone" in source or "Android" in source) and check_time(created_time):
            dicti[username]["coordinates"].append(coordinates)
            dicti[username]["text"].append(text)
        else:
            dicti[username]["text"].append(text)

    row = cursor.fetchone()

cursor = cnxn.cursor()
for username in dicti.keys():
    if len(dicti[username]["coordinates"]) > 20:
        center = get_center_in_cluster(dicti[username]["coordinates"])
        dicti[username]["home"] = center
        print dicti[username]["home"]
        # DO THIS FIRST
        execute_line = "INSERT INTO [LOCALITY1].[dbo].[twitter_users] (screenname, lat, lon) VALUES ('" + username + "', '" + str(
            dicti[username]["home"][0]) + "', '" + str(dicti[username]["home"][1]) + "')"
        # print(execute_line)
        cursor.execute(execute_line)
        cnxn.commit()



