# -*- coding: utf-8 -*-
import httplib2, json

def getTemperature(city, country):
    try:
        resp, content = httplib2.Http().request('http://api.openweathermap.org/data/2.5/weather?q='+city+","+country, "GET")
        contentObject = content.decode('utf-8')
        data = json.loads(contentObject) 
        return (" >> " + city.title() + "'s current temperature is: " + str(round((data['main']['temp'] - 273.15), 0)) + u" °C")
    except:
        return "Unable to get weather data."