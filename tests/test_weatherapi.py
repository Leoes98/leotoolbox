from leotoolbox.weatherapi import *

def test_search_city_for_paris():
    city = search_city('Paris')
    assert city['title'] == 'Paris'
    assert city['woeid'] == 615702

def test_search_city_for_london():
    city = search_city('London')
    assert city['title'] == 'London'
    assert city['woeid'] == 44418

def test_search_city_for_unknown_city():
    city = search_city('Rouen')
    assert city == None
