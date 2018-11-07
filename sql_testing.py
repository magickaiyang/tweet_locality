import pyodbc
from detect_bot import *
from dbscan_test import *

server = '128.46.137.201'
database = 'LOCALITY1'
username = 'localityedit'
password = 'Edit123'
cnxn = pyodbc.connect(
    'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()

cursor.execute("SELECT [created_at],[screen_name],[geo_lat],[geo_long],[tweet_text] FROM [LOCALITY1].[dbo].[Query]")
row = cursor.fetchone()

dicti = {}
c = 0
while row:
    created_time = row[0]
    username = row[1]
    coordinates = [row[2], row[3]]
    text = row[4]
    # if detectbot(username)<=2.5:
    if username not in dicti.keys():
        dicti.update({username: {"coordinates": [coordinates], "text": [text], "home": []}})
    else:
        dicti[username]["coordinates"].append(coordinates)
        dicti[username]["text"].append(text)

    row = cursor.fetchone()

count = 0

cursor = cnxn.cursor()
for username in dicti.keys():
    if len(dicti[username]["coordinates"]) > 20:
        count = count + 1
        center = get_center_in_cluster(dicti[username]["coordinates"])
        dicti[username]["home"] = center
        print dicti[username]["home"]
        # DO THIS FIRST
        execute_line = "INSERT INTO [LOCALITY1].[dbo].[twitter_users] (screenname, lat, lon) VALUES ('" + username + "', '" + str(
            dicti[username]["home"][0]) + "', '" + str(dicti[username]["home"][1]) + "')"
        # print(execute_line)
        cursor.execute(execute_line)
        cnxn.commit()

print (count)
