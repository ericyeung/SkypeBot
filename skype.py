# python skype.py [-r] 
# -*- coding: utf-8 -*-

import sys
import Skype4Py
import httplib2
import json
import re
import time
import threading
import argparse
import boto3
from datetime import datetime

from modules.answer_ball import get8BallAnswer
from modules.streamers_list import getStreamers, addStreamer, removeStreamer
from modules.weather import getTemperature
from modules.help import getHelpMessages
from modules.files import tryReading
from modules.hearthstone import getCardDescription
from modules.task_thread import TaskThread

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
        self.live = False
        threads = []
        for chat in self.skypeClient.BookmarkedChats:  # Looks in bookmarked chats and returns a list of all bookmarked chats
            if self.power and self.getIfValidGroup(chat._GetActiveMembers()):
                for streamer in sorted(getStreamers(), key=lambda x: x['name']): # Create a new thread for each api call
                    thread = threading.Thread(target=self.queryStreamer, args=[chat, streamer, False])
                    thread.start()
                    threads.append(thread)
                for thread in threads:
                    thread.join()
        
    """
    def print_checkin(self):
        for chat in self.skypeClient.BookmarkedChats:  # Looks in bookmarked chats and returns a list of all bookmarked chats
            if self.power and self.getIfValidGroup(chat._GetActiveMembers()):
                print("Checking in.")
                chat.SendMessage(" >> Today's message is: " + tryReading('MOTD.txt').read())
                chat.SendMessage(getTemperature("Toronto","Canada"))
                chat.SendMessage("#checkin")
                self.getLive(chat)
    """

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

    def getIfValidGroup(self, group_participants):
        participantsList = list(self.members)
        for member in group_participants:
            try:
                participantsList.remove(member._GetFullName())
            except:
                pass
        return not participantsList
        
    def start(self):
        while True:
            time.sleep(0.2)

    def command_callback(self, Message, Status):
        if Status == "SENT" or Status == "RECEIVED":
            chat = Message.Chat
            if self.getIfValidGroup(chat._GetActiveMembers()):
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
                        chat.SendMessage(" >> " + ", ".join(sorted(map(lambda x: x['display_name'], getStreamers()))))
                    elif message == "#checkin" and Status != "SENT":
                        chat.SendMessage(" >> Hello " + Message.Sender.FullName + "!" + " I am DaskBot!")
                    elif message.startswith("%addstreamer"):
                        splitMessage = messageUpper.strip().split(" ")
                        if (len(splitMessage) == 2):
                            resp, message = addStreamer(splitMessage[1])
                            if (resp):
                                chat.SendMessage(" >> " + splitMessage[1] + " added to list.")
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
                        chat.SendMessage(" >> Today's message is: " + tryReading('MOTD.txt').read())
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
                            f = open('MOTD.txt', 'w')
                            f.write(newMessage)
                            chat.SendMessage(" >> Today's message is: " + newMessage)
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