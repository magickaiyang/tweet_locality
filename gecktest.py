from selenium import webdriver
import json

def get_result():
    input_file = open("input.txt", "r")
    output_file = open("output.txt", "w")
    input_lines = input_file.readlines()

    browser = webdriver.Firefox()
    browser.get('http://geotxt.org/v2/')

    #sending input
    input_text = browser.find_element_by_id('queryText')

    for line in input_lines:
        input_text.send_keys(line)
        submit_button = browser.find_element_by_id('submitTextButton')
        submit_button.click()

        #getting result
        result_text = browser.find_elements_by_class_name('resultText')
        result_value=""
        for value in result_text:
           result_value+=value

        #making string to json data

        data = json.loads(result_value)

        #getting required output and stored in a file
        output_file.write(get_toponym(data))
        output_file.write(get_location(data))

        #instructions from: https://realpython.com/modern-web-automation-with-python-and-selenium/


    input_file.close()
    output_file.close()

def get_toponym(data):
    toponym = data['features']['0']['properties']['toponym']
    for hierarchy in data['features']['0']['properties']['hierarchy']['features']:
        toponym = toponym + ", " + hierarchy['properties']['toponym']

    return toponym


def get_location(data):
    return data['features']['0']['geometry']


get_result()


