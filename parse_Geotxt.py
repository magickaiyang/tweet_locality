import requests
import json

M_PARAMETER = 'm=gates&q='

def parse_text(line,option):
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
        print("Invalid input, using default stanfords")
        M_PARAMETER = 'm=stanfords&q='

    request_line = 'http://geotxt.org/v2/api/geotxt.json?' + M_PARAMETER + line
    print(request_line)
    r = requests.get(request_line)
    data = r.json()

    return data

    # toponyms = get_toponym(data)
    # locations = get_location(data)
    #
    # result = ""
    # for i in range(0, len(toponyms)):
    #     result += (str(i) + ": \n" + toponyms[i] + "\n" + str(locations[i]) + "\n\n")
    #
    # return result



def get_toponym(data):
    result = []
    for places in data['features']:
        toponym = places['properties']['toponym']
        for hierarchy in places['properties']['hierarchy']['features']:
            toponym = toponym + ", " + hierarchy['properties']['toponym']
        result.append(toponym)
    return result


def get_location(data):
    result = []
    for places in data['features']:
        result.append(json.dumps(places['geometry']))
    return result


#def main():
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

