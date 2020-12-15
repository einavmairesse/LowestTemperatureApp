from datetime import datetime, timezone, timedelta

import requests

from App import config


def get_timestamp(days_from_current):
    today = datetime.today()
    target_day = today - timedelta(days=days_from_current)
    year, month, day = target_day.year, target_day.month, target_day.day
    target_day_timestamp = datetime(year, month, day, tzinfo=timezone.utc).timestamp()
    return int(target_day_timestamp)


def get_api_url(lat, lon, timestamp):
    base_path = "https://api.openweathermap.org/data/2.5/onecall/timemachine?"
    final_path = '{base_path}lat={lat}&lon={lon}&dt={timestamp}&appid={token}'.format(
        base_path=base_path, lat=lat, lon=lon, timestamp=timestamp, token=config.token
    )

    return final_path


def get_coldest_day_context(coldest_hours_in_day):
    lowest_temperature_context = None
    min_temp = float('inf')

    for day in coldest_hours_in_day:
        if day['temp'] <= min_temp:
            min_temp = day['temp']
            lowest_temperature_context = day

    return lowest_temperature_context


def get_lowest_temp_in_city(city_coordinates, days_count):
    city_weather_data = []
    coldest_hours_in_day = []
    coldest_hour_context = None

    for day in range(0, days_count):
        day_timestamp = get_timestamp(day)
        api_url = get_api_url(lat=city_coordinates[0], lon=city_coordinates[1], timestamp=day_timestamp)
        response = execute_request(api_url)
        if response:
            city_weather_data.append(response.json())
        else:
            city_weather_data.append(None)

    for day in city_weather_data:
        coldest_hour_context = get_lowest_temp_in_day(day)
        coldest_hours_in_day.append(coldest_hour_context)
        # todo: need to determine the coldest day in the city (TODAY (14/12/2020 Israel time)!)
    coldest_day_context = get_coldest_day_context(coldest_hours_in_day)
    return coldest_day_context


def get_lowest_temp_in_day(day_context):
    lowest_temperature_context = None
    min_temp = float('inf')

    for hourly_entry in day_context['hourly']:
        if hourly_entry['temp'] <= min_temp:
            min_temp = hourly_entry['temp']
            lowest_temperature_context = hourly_entry

    return lowest_temperature_context


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


def get_coldest_city_by_context(city_to_weather_data):
    lowest_temp = float('inf')
    lowest_temp_city = None

    for city in city_to_weather_data:
        city_temp = city_to_weather_data[city]['temp']
        if city_temp < lowest_temp:
            lowest_temp = city_temp
            lowest_temp_city = city

    city_to_weather_data[lowest_temp_city]['city_name'] = lowest_temp_city
    return city_to_weather_data[lowest_temp_city]


def get_coldest_city_context(city_to_coordinates):
    city_to_weather_data = {}
    for city in city_to_coordinates:
        city_coordinates = city_to_coordinates[city]
        city_content = get_lowest_temp_in_city(city_coordinates, days_count=config.days_back)
        city_to_weather_data[city] = city_content

    coldest_city_context = get_coldest_city_by_context(city_to_weather_data)
    return coldest_city_context
