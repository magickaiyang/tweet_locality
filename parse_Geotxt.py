import pyodbc
import requests
import json
import multiprocessing
import time
import coordinate_to_country
# import find_boundary

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


def get_country_code(data):
    result = []
    for places in data['features']:
        result.append(places['properties']['countryCode'])
    return set(result)

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
# get percentage of tweets with place/ total number of tweets
#######
def tweets_percentage_of_place_in_usertable():
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

    cnxn3 = pyodbc.connect(
        'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor3 = cnxn3.cursor()

    # Write query and execute
    query = "SELECT [users],[tweet_count] FROM [LOCALITY1].[dbo].[twitter_users]"
    cursor.execute(query)

    # Start with getting the first row
    row = cursor.fetchone()

    while row:
        screen_name  = row[0]
        tweets_count = row[1]
        place_count = 0
        query2 = "SELECT * FROM [LOCALITY1].[dbo].[tweets] where screen_name = '" + screen_name + "'"
        cursor2.execute(query2)
        row2 = cursor2.fetchone()
        while row2:
            tweet_text = row2[4]
            if parse_text(tweet_text, "") is not None:
                place_count += 1

        percentage = float(place_count)/tweets_count
        query3 = "UPDATE [LOCALITY1].[dbo].[twitter_users] SET percent_place = " + str(percentage) + " WHERE users = '" + screen_name + "'"
        cursor3.execute(query3)
        row = cursor.fetchone()

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
        print(query2)

        cursor2.execute(query2)
        cnxn2.commit()

        row = cursor.fetchone()


def percentage_about_home_country():

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

    cnxn3 = pyodbc.connect(
        'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor3 = cnxn3.cursor()

    # Write query and execute
    query = "SELECT [users],[tweet_count],[country] FROM [LOCALITY1].[dbo].[twitter_users]"
    cursor.execute(query)

    # Start with getting the first row
    row = cursor.fetchone()

    while row:
        screen_name  = row[0]
        tweets_count = row[1]
        home_country = row[2]
        place_count = 0
        query2 = "SELECT * FROM [LOCALITY1].[dbo].[tweets] where screen_name = '" + screen_name + "'"
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
        query3 = "UPDATE [LOCALITY1].[dbo].[twitter_users] SET about_home = " + str(percentage) + " WHERE users = '" + screen_name + "'"
        cursor3.execute(query3)
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

    # one process per core
    pool = multiprocessing.Pool()

    while row:
        latitude = row[2]
        longitude = row[3]
        index = row[6]

        while len(pool._cache) >= multiprocessing.cpu_count():
            time.sleep(0.1)

        pool.apply_async(coordinate_to_country.locate_country, args=(longitude, latitude, index))

        row = cursor.fetchone()


#
if __name__ == '__main__':
    tweets_issued_in()
