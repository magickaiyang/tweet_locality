import pyodbc
import requests
import json
import find_boundary

M_PARAMETER = 'm=stanfords&q='


# Function to display, ask user's option of geo parsing method,
# and parse the text with selected option. (Default as gates)
# Return the Geotext Json data
def parse_text(line, option):
    if option == '1' or option == 'gates':
        M_PARAMETER = 'm=gates&q='
    elif option == '2' or option == 'stanfords':
        M_PARAMETER = 'm=stanfords&q='
    elif option == '3' or option == 'gate':
        M_PARAMETER = 'm=gate&q='
    elif option == '4' or option == 'stanford':
        M_PARAMETER = 'm=stanford&q='
    elif option == '5' or option == 'gateh':
        M_PARAMETER = 'm=gateh&q='
    elif option == '6' or option == 'stanfordh':
        M_PARAMETER = 'm=stanfordh&q='
    else:
        # print("Invalid input, using default stanfords")
        M_PARAMETER = 'm=stanfords&q='

    request_line = 'https://www.geovista.psu.edu/geotxt/api/geotxt.json?' + M_PARAMETER + line

    print(request_line)
    r = requests.get(request_line)
    # if r.status_code == 500:
    #     return None
    data = r.json()

    return data

# Function to get the toponym of given Geotext json data
def get_toponym(data):
    result = []
    for places in data['features']:
        toponym = places['properties']['toponym']
        for hierarchy in places['properties']['hierarchy']['features']:
            toponym = toponym + ", " + hierarchy['properties']['toponym']
        result.append(toponym)
    return result


# Function to get the location of given Geotext json data
def get_location(data):
    result = []
    for places in data['features']:
        result.append(json.dumps(places['geometry']))
    return result


# Main function to test the functions above, used the input.txt file
# def main():
    # input_file = open("input.txt", "r")
    # output_file = open("output.txt", "w")
    # input_lines = input_file.readlines()
    # input_file.close()
    # option = raw_input('Please choose from the following two NER engines and multiple methods:\n'
    #              '(1) "gates" (without quotation marks) for Gate and our improved ranking scheme\n'
    #              '(2) "stanfords" for Stanford NER and our improved ranking scheme\n'
    #              '(3) "gate" for default GeoNames ranking scheme with each NER engine\n'
    #              '(4) "stanford" for default GeoNames ranking scheme with each NER engine\n'
    #              '(5) "gateh" to enable place name disambiguation\n'
    #              '(6) "stanfordh" to enable place name disambiguation\n')
    #
    #
    # for line in input_lines:
    #     output_file.write(line)
    #     output_file.write(parse_text(line))
    #
    # output_file.close()


####
# Incomplete
#######
def tweets_percentage_in_usertable():
    server = '128.46.137.201'
    database = 'LOCALITY1'
    username = 'localityedit'
    password = 'Edit123'
    # Connect to database
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()

    cnxn2 = pyodbc.connect(
        'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor2 = cnxn2.cursor()

    # Write query and execute
    query = "SELECT [users],[home_lat],[home_lon] FROM [LOCALITY1].[dbo].[twitter_users]"
    cursor.execute(query)

    # Start with getting the first row
    row = cursor.fetchone()

    while row:
        screen_name  = row [0]
        tweets_count = 0
        place_count = 0
        query2 = "SELECT * FROM [LOCALITY1].[dbo].[tweets] where screen_name = '" + screen_name + "'"
        cursor2.execute(query2)
        row2 = cursor2.fetchone()
        while row2:
            tweet_text = row2[4]
            tweets_count += 1
            if parse_text(tweet_text, "") != None:
                place_count += 1


def place_count_in_tweets():
    server = '128.46.137.201'
    database = 'LOCALITY1'
    username = 'localityedit'
    password = 'Edit123'
    # Connect to database
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()

    cnxn2 = pyodbc.connect(
        'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor2 = cnxn2.cursor()

    query = "SELECT * FROM [LOCALITY1].[dbo].[tweets]"

    cursor.execute(query)
    row = cursor.fetchone()

    while row:

        tweet_text = row[4]
        id = row[6]
        geojson_data = parse_text(tweet_text, "")
        place_count = 0
        if geojson_data != None:
            place_count = len(geojson_data['features'])

        query2 = "UPDATE [LOCALITY1].[dbo].[tweets] SET place_count = " + str(place_count) + " WHERE id = " + str(id)
        print query2

        cursor2.execute(query2)
        cnxn2.commit()

        row = cursor.fetchone()

def tweets_issued_in():
    server = '128.46.137.201'
    database = 'LOCALITY1'
    username = 'localityedit'
    password = 'Edit123'
    # Connect to database
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()

    cnxn2 = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor2 = cnxn2.cursor()

    query = "SELECT * FROM [LOCALITY1].[dbo].[tweets]"

    cursor.execute(query)
    row = cursor.fetchone()

    while row:
        latitude = row[2]
        longitude = row[3]
        id = row[6]

        country = find_boundary.locate_country(longitude, latitude, 'maps/world_countries_2017')
        print('latitude: ', str(latitude), 'longitude:', str(longitude), 'country: ', country)
        # query2 = "UPDATE [LOCALITY1].[dbo].[tweets] SET issued_in = '" + country + "' WHERE id = " + str(id)
        # print query2
        # cursor2.execute(query2)
        # cnxn2.commit()

        row = cursor.fetchone()


# place_count_in_tweets()
#tweets_issued_in()
print(find_boundary.locate_country(-80.2358746, 26.224614, 'maps/world_countries_2017'))
