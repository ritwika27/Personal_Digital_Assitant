import requests as rq
import json
from weather_collection import *
from location import Location
from datetime import datetime 
import time

api_file = open("weather_api.txt", "r")
api_key = api_file.read()
api_file.close()

# exclude = "current,minutely,daily"
# url = "https://api.openweathermap.org/data/2.5/onecall?lat=39&lon=-78&exclude=%s&appid=%s&units=imperial" % (exclude, api_key)
# response = rq.get(url)
# data = json.loads(response.text)
# print(data["hourly"][0])


#exclude = "hourly,minutely,daily"
# url = "https://api.openweathermap.org/data/2.5/onecall?lat=39&lon=-78&appid=%s&units=imperial" % (api_key)
# response = rq.get(url)
# data = json.loads(response.text)
# print(data['minutely'])
loc = Location(35, -85)
start_time = datetime.now()
# x = get_current_weather_info(loc)
# print(x)

# y = get_weather_info(loc, start_time)
# print(y)

z = check_weather(loc)
print(z)

