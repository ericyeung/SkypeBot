# python skype.py [-r] 
# -*- coding: utf-8 -*-

import argparse
import boto3
import httplib2
import json
import re
import Skype4Py
import sys
import threading
import time
from datetime import datetime

from modules.answer_ball import get8BallAnswer
from modules.hearthstone import getCardDescription
from modules.help import getHelpMessages
from modules.motd import getMessage, updateMessage
from modules.streamers_list import getStreamers, addStreamer, removeStreamer
from modules.task_thread import TaskThread
from modules.weather import getTemperature

class SkypeBot():
    def __init__(self, members, periodic):
        self.skypeClient = Skype4Py.Skype()
        self.skypeClient.OnMessageStatus = self.command_callback
        self.skypeClient.Attach()
        self.members = members
        self.power = True
        self.streamer_state = {}
        if periodic:
            task = TaskThread(self.checkStreamers)
            # Run every minute
            task.setInterval(60)
            task.run()
    
    def checkStreamers(self):
        threads = []
        for chat in self.skypeClient.BookmarkedChats:  # Looks in bookmarked chats and returns a list of all bookmarked chats
            if self.power:
                for streamer in sorted(getStreamers(), key=lambda x: x['name']): # Create a new thread for each api call
                    thread = threading.Thread(target=self.queryStreamer, args=[chat, streamer, False])
                    thread.start()
                    threads.append(thread)
                for thread in threads:
                    thread.join()

    def getLive(self, chat):
        self.live = False
        threads = []
        for streamer in sorted(getStreamers(), key=lambda x: x['name']): # Create a new thread for each api call
            thread = threading.Thread(target=self.queryStreamer, args=[chat, streamer, True])
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        if not self.live:
            chat.SendMessage("No streamers are up! D:")

    def queryStreamer(self, chat, streamer, allStreamers=True):
        try:
            resp, content = httplib2.Http().request(streamer['stream'], "GET")
            contentObject = content.decode('utf-8')
            data = json.loads(contentObject)
            if (data['stream']):
                if allStreamers:
                    chat.SendMessage(streamer['display_name'] + "'s stream is up! - http://www.twitch.tv/" + streamer['name'])
                elif not self.streamer_state.get(streamer['name']):
                    chat.SendMessage(streamer['display_name'] + "'s stream is now online! - http://www.twitch.tv/" + streamer['name'])
                    self.streamer_state[streamer['name']] = True
                self.live = True
            else:
                if self.streamer_state.get(streamer['name']):
                    self.streamer_state[streamer['name']] = False
        except:
            pass
        
    def start(self):
        while True:
            time.sleep(0.2)

    def command_callback(self, Message, Status):
        if Status == "SENT" or Status == "RECEIVED":
            chat = Message.Chat
            message = Message.Body.lower()
            messageUpper = Message.Body
            if message == "%stopbot":
                self.power = False
                chat.SendMessage(" >> Goodbye. Zzz")
            elif message == "%startbot":
                self.power = True
                chat.SendMessage(" >> Hello World! I am back online!")
            elif self.power:
                if message == "%help":
                    for message in getHelpMessages():
                        chat.SendMessage(message)
                elif message == "%time":
                    chat.SendMessage(" >> " + datetime.now().strftime("%Y-%m-%d %H:%M %Z"))
                elif message == "%live":
                    self.getLive(chat)
                elif message.startswith("%8ball"):
                    chat.SendMessage(" >> " + get8BallAnswer() + ".")
                elif message == "%streamers":
                    chat.SendMessage(" >> " + ", ".join(item['display_name'] 
                                                        for item in sorted(getStreamers(),
                                                                           key=lambda x: x['name'])))
                elif message == "#checkin" and Status != "SENT":
                    chat.SendMessage(" >> Hello " + Message.Sender.FullName + "!" + " I am DaskBot!")
                elif message.startswith("%addstreamer"):
                    splitMessage = messageUpper.strip().split(" ")
                    if (len(splitMessage) == 2):
                        resp, message, display_name = addStreamer(splitMessage[1])
                        if (resp):
                            chat.SendMessage(" >> " + display_name + " added to list.")
                        else:
                            chat.SendMessage(" >> " + message)
                    else:
                        chat.SendMessage(" >> Invalid format.  %addstreamer [StreamerChannel]")
                elif message.startswith("%removestreamer"):
                    splitMessage = message.strip().split(" ")
                    if (len(splitMessage) == 2):
                        resp = removeStreamer(splitMessage[1]);
                        if resp:
                            chat.SendMessage(" >> " + splitMessage[1] + " removed from the list.")
                        else:
                            chat.SendMessage(" >> " + splitMessage[1] + " was not on the list.")
                    else:
                        chat.SendMessage(" >> Invalid format.  %removestreamer [StreamerChannel]")
                elif message == "%message":
                    chat.SendMessage(" >> Today's message is: " + getMessage())
                elif messageUpper.startswith("%trigger"):
                    chat.SendMessage(" >> [Trigger]" + messageUpper.replace("%trigger","",1))
                elif message.startswith("%weather"):
                    weather_message = message[9:]
                    splitMessage = weather_message.strip().split(",")
                    if (len(splitMessage) == 2):
                        chat.SendMessage(getTemperature(splitMessage[0].strip(), splitMessage[1].strip()))
                    else:
                        chat.SendMessage(" >> Invalid format.  %weather [City],[Country]")
                elif message.startswith("%message"):
                    newMessage = messageUpper[9:].encode('utf-8')
                    if(newMessage):
                        chat.SendMessage(" >> Today's message is: " + updateMessage(newMessage))
                elif message.startswith("%csgo"):
                    for i in range(4):
                        chat.SendMessage("GOGOGOGOGOGGO")
                elif message.startswith("%premade"):
                    chat.SendMessage(" >> Kaw Kaw KAW, calling all early birds")
                elif message.startswith("%wubwub"):
                    for i in range(4):
                        chat.SendMessage("WUBWUBWUBWUB")
                elif message.startswith("%kawkaw"):
                    for i in range(4):
                        chat.SendMessage("KAW AWH KAW AWH KAW AWH")
                elif '{' in message and '}' in message and 'hscard' not in message: #Hearthstone card information
                    results = re.findall(r'\{([^}]*)\}', message)
                    for item in results:
                        description = getCardDescription(item)
                        if description:
                            chat.SendMessage(" >> [HSCard] " + description)
                        else:
                            chat.SendMessage(" >> [HSCard] Cannot be found!  Please try again!")
                elif message.startswith("%code"):
                    chat.SendMessage(" >> It's time to CODE.")
                elif message.startswith("%"):
                    chat.SendMessage(" >> Invalid command. Type in %help for assistance.")

# Type in members of the groups you want to checkin with. 
#Eg. members = ['John Doe'] will #checkin to all favourited groups who have John Doe
members = []

parser = argparse.ArgumentParser()
parser.add_argument('-r', dest='periodic', action='store_true')
args = parser.parse_args()

# Create an instance of the Skype class.
SkypeBot(members, periodic=args.periodic).start()