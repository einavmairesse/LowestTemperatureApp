import requests

from App import config


def get_coldest_city_context():
    coldest_hour_in_every_city = []
    for city in config.cities:
        city_content = get_lowest_temp_in_city(city)
        coldest_hour_in_every_city.append(city_content)

    coldest_city_context = get_coldest_city_by_context(coldest_hour_in_every_city)
    return coldest_city_context


def get_coldest_city_by_context(cities_context):
    lowest_temp = float('inf')
    lowest_temp_main = None

    for city in cities_context:
        if city['temp_min'] < lowest_temp:
            lowest_temp = city['temp_min']
            lowest_temp_main = city
    return lowest_temp_main


def get_lowest_temp_in_city(city):
    city_weather_data = []
    api_url = get_api_url(city)
    response = execute_request(api_url)
    lowest_temp = float('inf')
    lowest_temp_main = None

    if response:
        city_weather_data.append(response.json())
    else:
        city_weather_data.append(None)
        # todo take care for missing data

    for hour_data in city_weather_data[0]['list']:
        if hour_data['main']['temp_min'] < lowest_temp:
            lowest_temp = hour_data['main']['temp_min']
            lowest_temp_main = hour_data['main']

    lowest_temp_main['city_name'] = city
    return lowest_temp_main


def get_api_url(city):
    base_path = "http://api.openweathermap.org/data/2.5/forecast?q="
    final_path = '{base_path}{city}&appid={token}'.format(
        base_path=base_path, city=city, token=config.token
    )
    return final_path


def execute_request(address):
    try:
        response = requests.get(address)
    except requests.exceptions.ConnectionError as e:
        # todo: Need to change print to logger
        print(e)
        return None
    if response.status_code != 200:
        response = None

    return response
