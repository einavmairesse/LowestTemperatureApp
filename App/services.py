from datetime import datetime, timedelta

import requests

from App import config


def get_coldest_city_content():
    coldest_hour_in_every_city = []
    for city in config.cities:
        weather_data = query_weather_data(city)
        city_content = get_lowest_temp_in_city(weather_data, city)
        coldest_hour_in_every_city.append(city_content)

    # check which city has the lowest temperature and return it's content
    coldest_city_content = get_coldest_city_by_content(coldest_hour_in_every_city)
    return coldest_city_content


def get_coldest_city_by_content(cities_content):
    lowest_temp = float('inf')
    lowest_temp_main = None

    for city in cities_content:
        if city['temp_min'] < lowest_temp:
            # for each city, save each current min temperature and it's content
            lowest_temp = city['temp_min']
            lowest_temp_main = city

    return lowest_temp_main


def get_lowest_temp_in_city(city_weather_data, city):
    lowest_temp = float('inf')
    lowest_temp_main = None

    for hour_data in city_weather_data['list']:
        # for every hour, save each current min temperature and it's content
        if hour_data['main']['temp_min'] < lowest_temp:
            lowest_temp = hour_data['main']['temp_min']
            lowest_temp_main = hour_data['main']

    lowest_temp_main['city_name'] = city
    return lowest_temp_main


def query_weather_data(city):
    # create the URL and execute the request
    api_url = get_api_url(city)
    response = execute_request(api_url)

    # Check if the request executed like expected.
    # If not, there was a problem in city's name or with connection- raising an exeption is necessary.
    if not response:
        raise Exception('There was a problem with URL. Check either connection or city''s name')
    return response.json()


def get_api_url(city):
    base_path = 'http://api.openweathermap.org/data/2.5/forecast?q='
    final_path = '{base_path}{city}&appid={token}'.format(
        base_path=base_path, city=city, token=config.api_token
    )
    return final_path


def execute_request(address):
    try:
        response = requests.get(address)
    except requests.exceptions.ConnectionError as e:
        print(e)
        return None
    if response.status_code != 200:
        response = None

    return response


def get_next_cache_flush():
    flush_hours = [0, 3, 6, 9, 12, 15, 18, 21]
    now = datetime.now()
    time_delta = 0

    for hour in flush_hours:
        # Determine the next flush interval.
        # Calculate time difference between current time and next flush.
        if hour - now.hour > 0:
            target = timedelta(hours=now.hour)
            now = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
            time_delta = target - now
            break

    return time_delta.seconds
