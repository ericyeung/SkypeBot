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

from modules.answer_ball import get_8_ball_answer
from modules.hearthstone import get_card_description
from modules.help import get_help_messages
from modules.motd import get_message, update_message
from modules.twitch import get_streamers, add_streamer, remove_streamer, get_all_live
from modules.task_thread import TaskThread
from modules.weather import getTemperature

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
    
    def check_streamers_continuously(self):
        threads = []
        if self.power:
            all_live = get_all_live()
            print(all_live)
            new_streamers = [stream for stream in all_live if stream not in self.live_streamers]
            print(new_streamers)
            for streamer in sorted(new_streamers, key=lambda x: x['name']):
                for chat in self.skypeClient.BookmarkedChats:
                    print("{}'s stream is now online! - http://www.twitch.tv/{}"
                          .format(streamer['display_name'], streamer['name']))
            self.live_streamers = list(all_live)

    def get_live(self, chat):
        all_live = get_all_live()
        if not all_live:
            chat.SendMessage("No streamers are up! D:")
        else:
            for streamer in all_live:
                chat.SendMessage("{}'s stream is up! - http://www.twitch.tv/{}"
                                 .format(streamer['display_name'], streamer['name']))

    def start(self):
        while True:
            time.sleep(0.2)

    def command_callback(self, Message, Status):
        if Status == "SENT" or Status == "RECEIVED":
            chat = Message.Chat
            message = Message.Body
            message_raw = Message.Body.lower()
            if message_raw == "%stopbot":
                self.power = False
                chat.SendMessage(" >> Goodbye. Zzz")
            elif message_raw == "%startbot":
                self.power = True
                chat.SendMessage(" >> Hello World! I am back online!")
            elif self.power:
                if message_raw == "%help":
                    for help_message in get_help_messages():
                        chat.SendMessage(help_message)
                elif message_raw == "%time":
                    chat.SendMessage(" >> " + datetime.now().strftime("%Y-%m-%d %H:%M %Z"))
                elif message_raw == "%live":
                    self.get_live(chat)
                elif message_raw.startswith("%8ball"):
                    chat.SendMessage(" >> " + get_8_ball_answer() + ".")
                elif message_raw == "%streamers":
                    chat.SendMessage(" >> " + ", ".join(item['display_name'] 
                                                        for item in sorted(get_streamers(),
                                                                           key=lambda x: x['name'])))
                elif message_raw == "#checkin" and Status != "SENT":
                    chat.SendMessage(" >> Hello " + Message.Sender.FullName + "!" + " I am DaskBot!")
                elif message_raw.startswith("%addstreamer"):
                    splitMessage = message.strip().split(" ")
                    if (len(splitMessage) == 2):
                        resp, resp_message, display_name = add_streamer(splitMessage[1])
                        if (resp):
                            chat.SendMessage(" >> " + display_name + " added to list.")
                        else:
                            chat.SendMessage(" >> " + resp_message)
                    else:
                        chat.SendMessage(" >> Invalid format.  %addstreamer [StreamerChannel]")
                elif message_raw.startswith("%removestreamer"):
                    splitMessage = message.strip().split(" ")
                    if (len(splitMessage) == 2):
                        resp = remove_streamer(splitMessage[1]);
                        if resp:
                            chat.SendMessage(" >> " + splitMessage[1] + " removed from the list.")
                        else:
                            chat.SendMessage(" >> " + splitMessage[1] + " was not on the list.")
                    else:
                        chat.SendMessage(" >> Invalid format.  %removestreamer [StreamerChannel]")
                elif message_raw == "%message":
                    chat.SendMessage(" >> Today's message is: " + get_message())
                elif message_raw.startswith("%message"):
                    newMessage = message[9:].encode('utf-8')
                    if(newMessage):
                        chat.SendMessage(" >> Today's message is: {}".format(update_message(newMessage)))
                elif message_raw.startswith("%trigger"):
                    chat.SendMessage(" >> [Trigger]" + message.replace("%trigger","",1))
                elif message_raw.startswith("%weather"):
                    weather_message = message[9:]
                    splitMessage = weather_message.strip().split(",")
                    if (len(splitMessage) == 2):
                        chat.SendMessage(getTemperature(splitMessage[0].strip(), splitMessage[1].strip()))
                    else:
                        chat.SendMessage(" >> Invalid format.  %weather [City],[Country]")
                elif message_raw.startswith("%csgo"):
                    for i in range(4):
                        chat.SendMessage("GOGOGOGOGOGGO")
                elif message_raw.startswith("%premade"):
                    chat.SendMessage(" >> Kaw Kaw KAW, calling all early birds")
                elif message_raw.startswith("%wubwub"):
                    for i in range(4):
                        chat.SendMessage("WUBWUBWUBWUB")
                elif message_raw.startswith("%kawkaw"):
                    for i in range(4):
                        chat.SendMessage("KAW AWH KAW AWH KAW AWH")
                elif '{' in message_raw and '}' in message_raw and 'hscard' not in message_raw: #Hearthstone card information
                    results = re.findall(r'\{([^}]*)\}', message_raw)
                    for item in results:
                        description = get_card_description(item)
                        if description:
                            chat.SendMessage(" >> [HSCard] " + description)
                        else:
                            chat.SendMessage(" >> [HSCard] Cannot be found!  Please try again!")
                elif message_raw.startswith("%code"):
                    chat.SendMessage(" >> It's time to CODE.")
                elif message_raw.startswith("%"):
                    chat.SendMessage(" >> Invalid command. Type in %help for assistance.")

parser = argparse.ArgumentParser()
parser.add_argument('-r', dest='periodic', action='store_true')
args = parser.parse_args()

# Create an instance of the Skype class.
SkypeBot(periodic=args.periodic).start()