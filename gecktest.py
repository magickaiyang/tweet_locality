from selenium import webdriver
import json

def get_result(lines):
    input_file = open("input.txt", "r")
    output_file = open("output.txt", "w")
    input_lines = input_file.readlines()
  
    browser = webdriver.Firefox()
    browser.get('http://geotxt.org/v2/')

    #sending input
    input_text = browser.find_element_by_id('inputText')

    for line in input_lines:
        input_text.send_keys(line)
        input_text.submit()

        #getting result
        result_text = browser.find_elements_by_class_name('resultText')
        #making string to json data
        data = json.loads(result_text)
        
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
