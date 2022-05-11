
import requests as rq
import json
from datetime import datetime 
import time

api_file = open("weather_api.txt", "r")
api_key = api_file.read()
api_file.close()

icon_code = '10d'
weather_icon_url = 'http://openweathermap.org/img/wn/'
url_2 = '@2x.png'

hour = 3600
day = 86400
min = 60

weather_trigger_params = {
    'temp': {"min": 30 , "max": 85 , "min_desc": "Bring a Jacket! It's cold!", "max_desc": "It's over 85 degrees today!"},
    'pop': {"min": 0, "max": 60,  "min_desc": "No rain today!", "max_desc": "Bring an umbrella! It's going to rain today!"}, 
    'humidity': {"min": 0, "max": 60,  "min_desc": "It's dry today!", "max_desc": "It's really humid today!"},
    'wind_speed': {"min": 0, "max": 7 ,  "min_desc": "There's no wind today", "max_desc": "Be careful! Its really windy!"}
}

# params:  datettime object as input
# returns: utc string
def convert_utc_to_unix(utc):
    return time.mktime(utc.timetuple())

# params: unix time as a string
# returns datetime object
def convert_unix_time_to_utc(unix_time):
    return datetime.fromtimestamp(unix_time, datetime.timezone.utc)

def getHourlyForecast(loc):
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=imperial" % (loc.lat, loc.lon, api_key)
    response = rq.get(url)
    data = json.loads(response.text)
    return data["hourly"]

def getCurrentForecast(loc):
    exclude = "minutely,daily"
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=%s&appid=%s&units=imperial" % (loc.lat, loc.lon, exclude, api_key)
    response = rq.get(url)
    data = json.loads(response.text)
    return data

class Weather:
    def __init__(self,temp = None, pop = None, humidity = None, wind_speed = None, description = None, weather_icon_url = None):
        self.temp = temp
        self.pop = pop
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.description = description
        self.weather_icon_url = weather_icon_url
    def __str__(self):
        return "temp: {}\tpop: {}\thumidity: {}\twind_speed: {}\tdescription: {}\tweather_icon_url {}".format(self.temp, self.pop, self.humidity,
        self.wind_speed, self.description, self.weather_icon_url)
    def format_dict(self): 
        return {"temp":self.temp, "pop": self.pop, "humidity": self.humidity, "wind_speed": self.wind_speed}

# return a weather object
def get_current_weather_info(loc):
    data = getCurrentForecast(loc)
    current = data["current"]
    icon_code = current['weather'][0]["icon"]
    url = weather_icon_url  + icon_code + url_2
    w = Weather(current["temp"], data["hourly"][0]["pop"] *100, current["humidity"], current["wind_speed"], current["weather"][0]["description"], url)
    return w

#returns a weather object    
def get_weather_info(loc, start_time):
    data = getHourlyForecast(loc)
    unix_time = convert_utc_to_unix(start_time) 
    w = Weather() 
    for forecast in data:
        unix_time = int(unix_time)
        if forecast["dt"] == unix_time - (unix_time % hour): 
            icon_code = forecast['weather'][0]['icon']
            url = weather_icon_url  + icon_code + url_2
            w = Weather(forecast["temp"], forecast["pop"] *100, forecast["humidity"], forecast["wind_speed"], forecast["weather"][0]["description"], url)
            return w

# check if the user needs to be notified about the current weather conditions 
def check_weather(weatherman):
    weather_data = getCurrentForecast(weatherman.curr_location)
    w = get_current_weather_info(weatherman.curr_location).format_dict()
    print(weatherman.notification_flags)
    alert = ""
    notif = ""
    notify = False
    is_alert = False
    for key in weather_trigger_params: 
        value = weather_trigger_params[key]
        if w[key] <=value["min"]: 
            notif += (value["min_desc"] + " ")
            # check if this condition was already triggered, if not notify
            if not weatherman.notification_flags[key]:
                notify = True
                weatherman.notification_flags[key] = True
        elif w[key] >= value["max"]:
            notif += (value["max_desc"] + " ")
             # check if this condition was already triggered, if not notify
            if not weatherman.notification_flags[key]:
                notify = True
                weatherman.notification_flags[key] = True
        # if there is no condition worth notifying set back to false
        else: 
            weatherman.notification_flags[key] = False
    print(weatherman.notification_flags)
    if "alerts" in weather_data: 
        for a in weather_data["alerts"]:
            alert += a['event']
        if weatherman.last_alert_msg == alert:
            is_alert = False
        else: is_alert = True
        
     
    return {"alert_msg": alert, "notification": notif, "notify": notify, "is_alert": is_alert}

