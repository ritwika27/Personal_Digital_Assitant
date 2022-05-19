import requests as rq
import json
from datetime import datetime 
import time
from location import Location
import weather_collection

api_file = open("weather_api.txt", "r")
api_key = api_file.read()
api_file.close()

icon_code = '10d'
weather_icon_url = 'http://openweathermap.org/img/wn/'
url_2 = '@2x.png'

loc  = Location(34, -76)

w = weather_collection.get_current_weather_info(loc)
print(w)