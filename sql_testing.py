import pyodbc
from detect_bot import *
server = 'voxel.ecn.purdue.edu'
database = 'sns_viz'
username = 'localityread'
password = 'Read123'
cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

cursor.execute("SELECT TOP 100 [created_at], [screen_name], [geo_lat], [geo_long], [tweet_text] FROM [sns_viz].[dbo].[tweet_us_2015_10_12] WHERE geo_lat!=0 AND geo_long != 0")
row = cursor.fetchone()

dict={}
c = 0
while row:
    created_time = row[0]
    username = row[1]
    coordinates = [row[2], row[3]]
    text = row[4]
    #if detectbot(username)<=2.5:
    if username not in dict.keys():
        dict.update({username: {"coordinates": [coordinates], "text": [text]}})
    else:
        dict[username]["coordinates"].append(coordinates)
        dict[username]["text"].append(text)

    row = cursor.fetchone()


print dict