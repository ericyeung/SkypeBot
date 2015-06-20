# -*- coding: utf-8 -*-

import httplib2, json
h = httplib2.Http()

def getTemperature(city, country):
    try:
        resp, content = h.request('http://api.openweathermap.org/data/2.5/weather?q='+city+","+country, "GET")
        contentObject = content.decode('utf-8')
        data = json.loads(contentObject) 
        return (" >> " + city.title() + "'s current temperature is: " + str(round((data['main']['temp'] - 273.15), 0)) + u" °C")
    except:
        return "Unable to get weather data."