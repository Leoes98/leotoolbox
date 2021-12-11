import sys
import urllib.parse
import requests

BASE_URI = "https://www.metaweather.com"


def search_city(query):
    '''Look for a given city and disambiguate between several candidates.
    Return one city (or None)'''
    url = urllib.parse.urljoin(BASE_URI, 'api/location/search/')
    response = requests.get(url, params={
        'query': query,
        'format': 'json'
    }).json()
    city = None
    if len(response) == 1:
        city = response[0]
    elif len(response) > 1:
        for i, cit in enumerate(response):
            print(f"{i+1}. {cit['title']}")
        query = input("Pick one city:\n> ")
        city = response[int(query) - 1]
    else:
        print('City not found.')
    return city


def weather_forecast(woeid):
    '''Return a 5-element list of weather forecast for a given woeid'''
    url = urllib.parse.urljoin(BASE_URI, f'api/location/{woeid}')
    response = requests.get(url).json()
    forecast = []
    for day in response["consolidated_weather"]:
        forecast.append({
            "applicable_date": day["applicable_date"],
            "weather_state_name": day["weather_state_name"],
            "the_temp": round(day["the_temp"], 1)
        })
    return forecast
