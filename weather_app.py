#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Weather App to check current weather conditions
User Functions: initiate, calculate_hottest_city, calculate_coldest_city
"""

import requests
import shutil
import os
import json
from api_key import API as API_KEY

API_PREFIX = '&appid='
URL = 'https://api.openweathermap.org/data/2.5/weather?'
DEGREETYPE = 'Celsius'


class Map:
    '''simple dictionary to class conversion, allowing limited namespace usage of keys as objects'''

    def __init__(self, city_names):

        for key in city_names:
            setattr(self, key, city_names[key])


class CityWeather:
    '''
    Class to map partially namespace mapped data to simple namespace format
    '''

    def __init__(self, weather_classes):
        self.name = weather_classes.name
        self.temp = weather_classes.temp
        self.humidity = weather_classes.humidity
        self.max_temp = weather_classes.temp_max
        self.min_temp = weather_classes.temp_min
        pass


def pull_weather_data(zip_code, country='us', units='metric'):
    '''API Call from weather data website
    ARGS: zip_code (str), country (str), units (str)
    RETURNS: weather_data (dict)
    '''
    api_url = URL + 'zip=' + str(zip_code)  # URL plus zipcode
    # adding country and units of measure
    api_url += f',{country}' + f'&units={units}'
    api_url += API_PREFIX + API_KEY
    try:
        weather_data = requests.get(api_url).json()
        connection_code = weather_data['cod']
        if connection_code != 200:  # response code
            raise ValueError
    except ValueError:
        print(f'Bad response from API server [ERROR CODE {connection_code}]')
    print(f'Pulling data for zip code: {zip_code}')
    return weather_data


def initiate():
    '''Program startup routine, 
    build class_dict dictionary, 
    generate zipcode_list from file zip_codes.txt
    perform API data pull,
    dump API data to .json files,
    move json files to /data,
    read json files to memory,
    instantiate class to map json dictionary to namespace format,
    copy mapped dictionaries to weather_data dictionary,
    generate dictionary with city names as keys and zip codes as values,
    instantiate class to map city_names dictionary to namespace format,
    and finally perform combination of both namespace classes then map the resulting classes to global variables
    '''
    try:
        class_dict = {}
        print('Loading zip code weather data')
        zipcode_list = []
        with open('zip_codes.txt', 'r') as zipcodes:
            for zipcode in zipcodes:
                zipcode = zipcode.strip('\n')
                zipcode_list.append(zipcode)
                weather_data = pull_weather_data(zipcode)
                with open(f'Zipcode-{zipcode}.json', 'w') as myfile:
                    json.dump(weather_data, myfile, indent=2)
                move_file_to_data(zipcode)
            for zipcode in zipcode_list:
                class_dict[zipcode] = read_json(zipcode)
                class_dict[zipcode] = Map(class_dict[zipcode])
                print(f'Retrieve information from: {class_dict[zipcode].name} city')
            weather_data = class_dict
            city = city_names(weather_data)
            globals()['city'] = city
            cityClass = Map(city)
            map_to_globals(city, weather_data)
            print('Weather data successfully loaded')
    except:
        print('Error Occurred')


def read_json(filename):
    '''json file reading and returning read data

    ARGS: filename (str)
    '''
    path = (f'data/Zipcode-{filename}.json').replace('\n', '')
    with open(path, 'r') as json_file:
        filedata = json.load(json_file)
    return filedata


def move_file_to_data(zipcode):
    ''' Move files from root to data folder

    ARGS: zipcode (str)
    '''
    directory = os.path.abspath(__file__)
    filename = f'Zipcode-{zipcode}.json'
    # Find current path and write to variable 'path'
    dirsplit = (directory.split('/'))
    directory = dirsplit[0:-1]
    directory.append(filename)
    path = '/'.join(directory)
    # Repeat same process as 'path' but add folder 'data' before file name and write to 'data_path'
    data_directory = (directory[0:-1])
    data_directory.append(f'data')
    data_directory.append(filename)
    data_path = '/'.join(data_directory)
    shutil.move(path, data_path)


def city_names(weather_data):
    '''Iterate over weather data to generate a dictionary with 
    city names as keys having values that are their zip codes
    ARGS: weather_data (dict)
    '''
    city = {}
    for key in weather_data:
        city[weather_data[key].name] = key
    return city


def map_to_globals(city, weather_data):
    '''Iterate over values in city(dict) and weather_data(dict) to generate a dictionary of class instances from 
    Weather and create global variables of city names tied to those instances
    ARGS: city (dict), weather_data (dict)
    '''
    weather = {}
    weather_classes = {}

    for key in city:
        city_weather_data = {}
        city_weather_data['name'] = key
        city_weather_data['temp'] = (weather_data[city.get(key)].main['temp'])
        city_weather_data['temp_max'] = (
            weather_data[city.get(key)].main['temp_max'])
        city_weather_data['temp_min'] = (
            weather_data[city.get(key)].main['temp_min'])
        city_weather_data['humidity'] = str(
            (weather_data[city.get(key)].main['humidity'])) + str('%')
        weather[key] = city_weather_data
        weather_classes[key] = Map(weather[key])
        globals()[key] = CityWeather(weather_classes[key])


def calculate_hottest_city():
    '''Calculate the hottest city through iteration and replacing the variable 'hottest' with the highest temperature found. then output message to terminal'''
    temptype = 'hottest'
    hottest = 0.0
    for key in city:
        key = globals()[key]

        if float((key).temp) > hottest:
            hottest = (key.temp)
            hottest_city = key.name

    hot_city = (globals()[hottest_city])
    message = f'''The {temptype} city is {hot_city.name} with a current conditions {hot_city.name} has a temperature of {hot_city.temp} degrees {DEGREETYPE}
with a humidity of {hot_city.humidity}, a max temp of {hot_city.max_temp} degrees {DEGREETYPE}, and a min temp of {hot_city.min_temp} degrees {DEGREETYPE}'''
    print(message)
    pass


def calculate_coldest_city():
    '''Calculate the coldest city through iteration and replacing the variable 'coldest' with the coldest temperature found. then output message to terminal'''
    temptype = 'coldest'
    coldest = 999.0
    for key in city:
        key = globals()[key]

        if float((key).temp) < coldest:
            coldest = (key.temp)
            coldest_city = key.name

    cold_city = (globals()[coldest_city])
    message = f'''The {temptype} city is {cold_city.name} with a current conditions {cold_city.name} has a temperature of {cold_city.temp} degrees {DEGREETYPE}
with a humidity of {cold_city.humidity}, a max temp of {cold_city.max_temp} degrees {DEGREETYPE}, and a min temp of {cold_city.min_temp} degrees {DEGREETYPE}'''
    print(message)
    pass


if __name__ == '__main__':
    pass
