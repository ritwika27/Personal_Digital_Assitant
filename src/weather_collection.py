import requests as rq
import json
from datetime import datetime 
import time

api_key = '46174eb744bf1b113afbf6ddb0108b7d'

def getHourlyForecast(lat, lon):
    exclude = "current,minutely,daily"
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=%s&appid=%s&units=imperial" % (lat, lon, exclude, api_key)
    response = rq.get(url)
    data = json.loads(response.text)
    return data["hourly"]

def getCurrentForecast(lat, lon):
    exclude = "hourly,minutely,daily"
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=%s&appid=%s&units=imperial" % (lat, lon, exclude, api_key)
    response = rq.get(url)
    data = json.loads(response.text)
    return data["current"]

# params:  datettime object as input
# returns: utc string
def convert_utc_to_unix(utc):
    return time.mktime(utc.timetuple())

# params: unix time as a string
# returns datetime object
def convert_unix_time_to_utc(unix_time):
    return datetime.fromtimestamp(unix_time, datetime.timezone.utc)

#for demo, returns an array with [temp, precip, wind_speed]
def get_current_weather_info(lat, lon): 
    data = getHourlyForecast(lat, lon)
    #unix_time = convert_utc_to_unix(start_time)
    weather = []
    # for forecast in data: 
    #     if forecast["dt"] == int(unix_time): 
    #         weather = [forecast["temp"], forecast["rain"], forecast["wind_speed"]]
    #         break
    forecast = data[0]
    weather = [forecast["temp"], forecast["humidity"], forecast["wind_speed"]]
    return weather



def createTrigger():
    #TODO
    pass

def monitorTriggers():
    #TODO 
    pass

