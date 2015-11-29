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
import subprocess

from datetime import datetime

from modules.answer_ball import get_8_ball_answer
from modules.hearthstone import get_card_description
from modules.help import get_help_messages
from modules.motd import get_message, update_message
from modules.twitch import get_streamers, add_streamer, remove_streamer, get_all_live
from modules.task_thread import TaskThread
from modules.weather import get_temperature

class SkypeBot():
    def __init__(self, periodic):
        self.skypeClient = Skype4Py.Skype()
        self.skypeClient.OnMessageStatus = self.command_callback
        self.skypeClient.Attach()
        self.power = True
        self.live_streamers = []
        if periodic:
            task = TaskThread(self.check_streamers_continuously)
            # Run every minute
            task.setInterval(60)
            task.run()
    
    def sendMessage(self, chat, msg):
        if not args.test:
            chat.SendMessage(msg)
        else:
            print(msg)
    
    def check_streamers_continuously(self):
        threads = []
        if self.power:
            all_live = get_all_live()
            new_streamers = [stream for stream in all_live if stream not in self.live_streamers]
            for streamer in sorted(new_streamers, key=lambda x: x['name']):
                for chat in self.skypeClient.BookmarkedChats:
                    self.sendMessage(chat, "{}'s stream is now online! - http://www.twitch.tv/{}"
                                            .format(streamer['display_name'], streamer['name']))
            self.live_streamers = list(all_live)

    def get_live(self, chat):
        all_live = get_all_live()
        if not all_live:
            self.sendMessage(chat, "No streamers are up! D:")
        else:
            for streamer in all_live:
                self.sendMessage(chat, "{}'s stream is up! - http://www.twitch.tv/{}"
                                        .format(streamer['display_name'], streamer['name']))

    def start(self):
        while True:
            time.sleep(0.2)

    def command_callback(self, Message, Status):
        chat = Message.Chat
        if chat in set(self.skypeClient.BookmarkedChats) and (Status == "SENT" or Status == "RECEIVED"):
            message = Message.Body
            message_raw = Message.Body.lower()
            if message_raw == "%stopbot":
                self.power = False
                self.sendMessage(chat, " >> Goodbye. Zzz")
            elif message_raw == "%startbot":
                self.power = True
                self.sendMessage(chat, " >> Hello World! I am back online!")
            elif self.power:
                if message_raw == "%help":
                    for help_message in get_help_messages():
                        self.sendMessage(chat, help_message)
                elif message_raw == "%time":
                    self.sendMessage(chat, " >> " + datetime.now().strftime("%Y-%m-%d %H:%M %Z"))
                elif message_raw == "%live":
                    self.get_live(chat)
                elif message_raw.startswith("%8ball"):
                    self.sendMessage(chat, " >> " + get_8_ball_answer() + ".")
                elif message_raw == "%streamers":
                    self.sendMessage(chat, " >> " + ", ".join(item['display_name'] 
                                                        for item in sorted(get_streamers(),
                                                                           key=lambda x: x['name'])))
                elif message_raw == "#checkin" and Status != "SENT":
                    self.sendMessage(chat, " >> Hello " + Message.Sender.FullName + "!" + " I am DaskBot!")
                elif message_raw.startswith("%addstreamer"):
                    splitMessage = message_raw.strip().split(" ")
                    if (len(splitMessage) == 2):
                        resp, resp_message, display_name = add_streamer(splitMessage[1])
                        if (resp):
                            self.sendMessage(chat, " >> " + display_name + " added to list.")
                        else:
                            self.sendMessage(chat, " >> " + resp_message)
                    else:
                        self.sendMessage(chat, " >> Invalid format.  %addstreamer [StreamerChannel]")
                elif message_raw.startswith("%removestreamer"):
                    splitMessage = message.strip().split(" ")
                    if (len(splitMessage) == 2):
                        resp = remove_streamer(splitMessage[1]);
                        if resp:
                            self.sendMessage(chat, " >> " + splitMessage[1] + " removed from the list.")
                        else:
                            self.sendMessage(chat, " >> " + splitMessage[1] + " was not on the list.")
                    else:
                        self.sendMessage(chat, " >> Invalid format.  %removestreamer [StreamerChannel]")
                elif message_raw == "%message":
                    self.sendMessage(chat, " >> Today's message is: " + get_message())
                elif message_raw.startswith("%message"):
                    newMessage = message[9:].encode('utf-8')
                    if(newMessage):
                        self.sendMessage(chat, " >> Today's message is: {}".format(update_message(newMessage)))
                elif message_raw.startswith("%trigger"):
                    self.sendMessage(chat, " >> [Trigger]" + message.replace("%trigger","",1))
                elif message_raw.startswith("%weather"):
                    weather_message = message[9:]
                    splitMessage = weather_message.strip().split(",")
                    if (len(splitMessage) == 2):
                        self.sendMessage(chat, get_temperature(splitMessage[0].strip(), splitMessage[1].strip()))
                    else:
                        self.sendMessage(chat, " >> Invalid format.  %weather [City],[Country]")
                elif message_raw.startswith("%csgo"):
                    for i in range(4):
                        self.sendMessage(chat, "GOGOGOGOGOGGO")
                elif message_raw.startswith("%premade"):
                    self.sendMessage(chat, " >> Kaw Kaw KAW, calling all early birds")
                elif message_raw.startswith("%wubwub"):
                    for i in range(4):
                        self.sendMessage(chat, "WUBWUBWUBWUB")
                elif message_raw.startswith("%kawkaw"):
                    for i in range(4):
                        self.sendMessage(chat, "KAW AWH KAW AWH KAW AWH")
                elif '{' in message_raw and '}' in message_raw and 'hscard' not in message_raw: #Hearthstone card information
                    results = re.findall(r'\{([^}]*)\}', message_raw)
                    for item in results:
                        description = get_card_description(item)
                        if description:
                            self.sendMessage(chat, " >> [HSCard] " + description)
                        else:
                            self.sendMessage(chat, " >> [HSCard] Cannot be found!  Please try again!")
                elif message_raw.startswith("%code"):
                    self.sendMessage(chat, " >> It's time to CODE.")
                elif message_raw.startswith("%"):
                    self.sendMessage(chat, " >> Invalid command. Type in %help for assistance.")

parser = argparse.ArgumentParser()
parser.add_argument('-r', dest='periodic', action='store_true')
parser.add_argument('-t', dest='test', action='store_true')
args = parser.parse_args()

if args.test:
    print("Testing mode!")

# Create an instance of the Skype class.
SkypeBot(periodic=args.periodic).start()