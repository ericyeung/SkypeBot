import Skype4Py
import threading
import httplib2, json
from datetime import datetime
from answer_ball import get8BallAnswer
from streamers_list import streamerList, addStreamer, removeStreamer
from weather import getTemperature
from help import getHelpMessages

def print_checkin(participants):
    for elem in skypeClient.BookmarkedChats:  # Looks in bookmarked chats and returns a list of all bookmarked chats
        if getIfValidGroup(participants, elem._GetActiveMembers()):
            print("Checking in.")
            f = open('MOTD.txt', 'r').read()
            elem.SendMessage(" >> Today's message is: " + f)
            elem.SendMessage(getTemperature("Toronto","CA"))
            elem.SendMessage("#checkin")
            getLive(elem)

def getIfValidGroup(white_list, group_participants):
    participantsList = list(white_list)
    for member in group_participants:
        try:
            participantsList.remove(member._GetFullName())
        except:
            pass
    return not participantsList

def getLive(elem):
    numLiveStreamers = {'value': 0}
    threads = []
    for streamer in sorted(streamerList):
        thread = threading.Thread(target=queryStreamer, args=[elem, streamer, streamerList, numLiveStreamers])
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    if numLiveStreamers['value'] == 0:
        elem.SendMessage("No streamers are up! D:")

def queryStreamer(elem, streamer, streamerList, numLiveStreamers):
    try:
        h = httplib2.Http()
        resp, content = h.request(streamerList[streamer], "GET")
        contentObject = content.decode('utf-8')
        data = json.loads(contentObject) 
        if (data['stream']):
            elem.SendMessage(streamer + "'s stream is up! - http://www.twitch.tv/" + streamer)
            numLiveStreamers['value'] += 1
    except:
        pass

def Commands(Message, Status):
    if Status == "SENT" or Status == "RECEIVED":
        for elem in skypeClient.BookmarkedChats:
            if getIfValidGroup(members, elem._GetActiveMembers()):
                message = Message.Body.lower()
                print(Message.Body)
                if Message.Chat == elem:
                    if message == "%help":
                        for message in getHelpMessages():
                            elem.SendMessage(message)
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
                        for i in range(4):
                            elem.SendMessage("GOGOGOGOGOGGO")
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
