# python skype.py [-r] 
import sys
import Skype4Py
import threading
import httplib2, json
import re

from datetime import datetime
from answer_ball import get8BallAnswer
from streamers_list import streamerList, addStreamer, removeStreamer
from weather import getTemperature
from help import getHelpMessages
from files import tryReading
from hearthstone import getCardDescription

def print_checkin(participants):
    for chat in skypeClient.BookmarkedChats:  # Looks in bookmarked chats and returns a list of all bookmarked chats
        if botPower.get_power() and getIfValidGroup(participants, chat._GetActiveMembers()):
            print("Checking in.")
            chat.SendMessage(" >> Today's message is: " + tryReading('MOTD.txt').read())
            chat.SendMessage(getTemperature("Toronto","CA"))
            chat.SendMessage("#checkin")
            getLive(chat)

def getIfValidGroup(white_list, group_participants):
    participantsList = list(white_list)
    for member in group_participants:
        try:
            participantsList.remove(member._GetFullName())
        except:
            pass
    return not participantsList

def getLive(chat):
    numLiveStreamers = {'value': 0} # Act as a pointer when passed into function
    threads = []
    for streamer in sorted(streamerList): # Create a new thread for each api call
        thread = threading.Thread(target=queryStreamer, args=[chat, streamer, streamerList, numLiveStreamers])
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    if numLiveStreamers['value'] == 0:
        chat.SendMessage("No streamers are up! D:")

def queryStreamer(chat, streamer, streamerList, numLiveStreamers):
    try:
        resp, content = httplib2.Http().request(streamerList[streamer], "GET")
        contentObject = content.decode('utf-8')
        data = json.loads(contentObject) 
        if (data['stream']):
            chat.SendMessage(streamer + "'s stream is up! - http://www.twitch.tv/" + streamer)
            numLiveStreamers['value'] += 1
    except:
        pass

def Commands(Message, Status):
    if Status == "SENT" or Status == "RECEIVED":
        chat = Message.Chat
        if getIfValidGroup(members, chat._GetActiveMembers()):
            message = Message.Body.lower()
            messageUpper = Message.Body
            if message == "%stopbot":
                botPower.set_power(False)
                chat.SendMessage(" >> Goodbye. Zzz")
            elif message == "%startbot":
                botPower.set_power(True)
                chat.SendMessage(" >> Hello World! I am back online!")
            elif botPower.get_power():
                if message == "%help":
                    for message in getHelpMessages():
                        chat.SendMessage(message)
                elif message == "%time":
                    chat.SendMessage(" >> " + datetime.now().strftime("%Y-%m-%d %H:%M %Z"))
                elif message == "%live":
                    getLive(chat)
                elif message.startswith("%8ball"):
                    chat.SendMessage(" >> " + get8BallAnswer() + ".")
                elif message == "%streamers":
                    chat.SendMessage(" >> " + ", ".join(sorted(streamerList.keys())))
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
                #elif messageUpper.startswith("%trigger"):
                #    chat.SendMessage(" >> [Trigger]" + messageUpper.replace("%trigger","",1))
                elif message.startswith("%weather"):
                    splitMessage = message.strip().split(" ")
                    if (len(splitMessage) == 3):
                        chat.SendMessage(getTemperature(splitMessage[1], splitMessage[2]))
                    else:
                        chat.SendMessage(" >> Invalid format.  %weather [City] [Country]")
                elif message.startswith("%message"):
                    newMessage = messageUpper[messageUpper.find('%message ')+9:].decode('utf-8')
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
                elif '[' in message and ']' in message and 'hscard' not in message: #Hearthstone card information
                    results = re.findall(r'\[([^]]*)\]', message)
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

class botPowerButton():
    def __init__(self, power):
        self.power = power

    def set_power(self, power):
        self.power = power

    def get_power(self):
        return self.power

# Type in members of the groups you want to checkin with. 
#Eg. members = ['John Doe'] will #checkin to all favourited groups who have John Doe
members = []

botPower = botPowerButton(True)

# Create an instance of the Skype class.
skypeClient = Skype4Py.Skype()
skypeClient.OnMessageStatus = Commands
skypeClient.Attach()

if len(sys.argv) > 2 and sys.argv[2] == '-r':
    task = TaskThread(print_checkin, members)
    task.run()

while True: # Infinite loop to catch commands
    pass
