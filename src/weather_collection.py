import requests as rq
import json
from datetime import datetime 
import time

api_key = '46174eb744bf1b113afbf6ddb0108b7d'

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
    exclude = "current,minutely,daily"
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=%s&appid=%s&units=imperial" % (lat, lon, exclude, api_key)
    response = rq.get(url)
    data = json.loads(response.text)

    hour = convert_unix_time_to_utc(data["hourly"][0]["dt"])
    
    hourly = ["hourly"][0]
    weather = [ hourly["temp"], hourly["rain"], hourly["wind_speed"] ]
    
    return weather

class Location: 
    def __init__(self, lat, lon, start_time, end_time):
        self.lat = lat
        self.lon = lon
        self.start_time = start_time
        self.end_time  = end_time
        self.triggers = []

    def createTrigger():
        #TODO
        pass

    def monitorTriggers():
        #TODO 
        pass

    def getHourlyForecast(self):
        exclude = "current,minutely,daily"
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=%s&appid=%s&units=imperial" % (self.lat, self.lon, exclude, api_key)
        response = rq.get(url)
        data = json.loads(response.text)
        return data["hourly"]
    
    def getCurrentForecast(self):
        exclude = "hourly,minutely,daily"
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=%s&appid=%s&units=imperial" % (self.lat, self.lon, exclude, api_key)
        response = rq.get(url)
        data = json.loads(response.text)
        return data["current"]
