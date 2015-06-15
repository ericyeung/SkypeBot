# -*- coding: utf-8 -*-

import Skype4Py
import threading
import httplib2, json
from datetime import datetime
from answer_ball import get8BallAnswer
from streamers_list import streamerList, addStreamer, removeStreamer

def print_checkin(participants):
    for elem in skypeClient.BookmarkedChats:  # Looks in bookmarked chats and returns a list of all bookmarked chats
        if getIfValidGroup(participants, elem._GetActiveMembers()):
            print("Checking in.")
            f = open('MOTD.txt', 'r').read()
            elem.SendMessage(" >> Today's message is: " + f)
            elem.SendMessage(getTemperature("Toronto","CA"))
            elem.SendMessage("#checkin")
            getLive(elem)    


def getTemperature(city, country):
    print('http://api.openweathermap.org/data/2.5/weather?q='+city+","+country)
    resp, content = h.request('http://api.openweathermap.org/data/2.5/weather?q='+city+","+country, "GET")
    try:
        contentObject = content.decode('utf-8')
        data = json.loads(contentObject) 
        return (" >> " + city.title() + "'s current temperature is: " + str(round((data['main']['temp'] - 273.15), 0)) + u" °C")
    except:
        return "Unable to get weather data."

def getIfValidGroup(white_list, group_participants):
    participantsList = list(white_list)
    for member in group_participants:
            try:
                participantsList.remove(member._GetFullName())
            except:
                pass
    return not participantsList

def getLive(elem):
    numLiveStreamers = 0
    for streamer in streamerList:
        resp, content = h.request(streamerList[streamer], "GET")
        try:
            contentObject = content.decode('utf-8')
            data = json.loads(contentObject) 
            if (data['stream']):
                elem.SendMessage(streamer + "'s stream is up! - http://www.twitch.tv/" + streamer)
                numLiveStreamers += 1
        except:
            pass
    if numLiveStreamers == 0:
        elem.SendMessage("No streamers are up! D:")

def Commands(Message, Status):
    if Status == "SENT" or Status == "RECEIVED":
        for elem in skypeClient.BookmarkedChats:
            if getIfValidGroup(members, elem._GetActiveMembers()):
                message = Message.Body.lower()
                print(message)
                if Message.Chat == elem:
                    if message == "%help":
                        elem.SendMessage(" >> %time - Gets the current time(To be formatted)")
                        elem.SendMessage(" >> %live - Gets the livestreamers.")
                        elem.SendMessage(" >> %8ball [question] - Need an answer? Consult 8Ball.")
                        elem.SendMessage(" >> %streamers - Gives a list of streamers currently being polled.")
                        elem.SendMessage(" >> %addstreamer [streamer's channel] - Adds a streamer to the list of watched streamers.")
                        elem.SendMessage(" >> %removestreamer [streamer's channel] - Removes a streamer to the list of watched streamers.")
                        elem.SendMessage(" >> %message [optional message]- Shows/Modifies the message of the day.")
                        elem.SendMessage(" >> %weather [city] [country] - Gets the weather for a city in a country.")
                    elif message == "%time":
                        elem.SendMessage(" >> " + datetime.now().strftime("%Y-%m-%d %H:%M %Z"))
                    elif message == "%live":
                        getLive(elem)
                    elif message.startswith("%8ball"):
                        elem.SendMessage(" >> " + get8BallAnswer() + ".")
                    elif message == "%streamers":
                        elem.SendMessage(" >> " + ", ".join(sorted(streamerList.keys())))
                    elif message.startswith("%addstreamer"):
                        splitMessage = message.strip().split(" ")
                        if (len(splitMessage) == 2):
                            resp, message = addStreamer(splitMessage[1])
                            if (resp):
                                elem.SendMessage(" >> " + splitMessage[1] + " added to list.")
                            else:
                                elem.SendMessage(" >> " + message)
                        else:
                            elem.SendMessage(" >> Invalid format.  %addstreamer [StreamerChannel]")
                    elif message.startswith("%removestreamer"):
                        splitMessage = message.strip().split(" ")
                        if (len(splitMessage) == 2):
                            resp = removeStreamer(splitMessage[1]);
                            if resp:
                                elem.SendMessage(" >> " + splitMessage[1] + " removed from the list.")
                            else:
                                elem.SendMessage(" >> " + splitMessage[1] + " was not on the list.")
                        else:
                            elem.SendMessage(" >> Invalid format.  %removestreamer [StreamerChannel]")
                    elif message == "%message":
                        f = open('MOTD.txt', 'r').read()
                        elem.SendMessage(" >> Today's message is: " + f)
                    elif message.startswith("%weather"):
                        splitMessage = message.strip().split(" ")
                        if (len(splitMessage) == 3):
                            elem.SendMessage(getTemperature(splitMessage[1], splitMessage[2]))
                        else:
                            elem.SendMessage(" >> Invalid format.  %weather [City] [Country]")
                    elif message.startswith("%message"):
                        newMessage = message[message.find('%message ')+9:].decode('utf-8')
                        if(newMessage):
                            f = open('MOTD.txt', 'w')
                            f.write(newMessage)
                            elem.SendMessage(" >> Today's message is: " + newMessage)
                    elif message.startswith("%csgo"):
                        
                    elif message.startswith("%"):
                        elem.SendMessage(" >> Invalid command. Type in %help for assistance.")

class TaskThread(threading.Thread):
    """Thread that executes a task every N seconds"""
    
    def __init__(self, task, args):
        threading.Thread.__init__(self)
        self._finished = threading.Event()
        self._interval = 3600
        self.task = task
        self.args = args
    
    def setInterval(self, interval):
        """Set the number of seconds we sleep between executing our task"""
        self._interval = interval
    
    def run(self):
        while 1:
            if self._finished.isSet(): return
            self.task(self.args)
            self._finished.wait(self._interval)

h = httplib2.Http()
# Type in members of the groups you want to checkin with. 
#Eg. members = ['John Doe'] will #checkin to all favourited groups who have John Doe
members = []

# Create an instance of the Skype class.
skypeClient = Skype4Py.Skype()
skypeClient.OnMessageStatus = Commands
skypeClient.Attach()

task = TaskThread(print_checkin, members)
task.run()

while True: # Infinite loop to catch commands
    pass
