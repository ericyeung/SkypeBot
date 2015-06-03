import Skype4Py
import threading
import httplib2, json

streamersList = ['Windask','LightBrite','DragonSlayer965', 'Kin_Tsuna', 'iGumdrop', 'OGKhey', 'itsHafu', "AkumaLuffy", "nl_Kripp"]
streamerList = {}

for streamer in streamersList:
    streamerList[streamer] = 'https://api.twitch.tv/kraken/streams/' + streamer

def print_checkin(participants):
    for elem in skypeClient.BookmarkedChats:  # Looks in bookmarked chats and returns True if chat is found.
        participantsList = list(participants)
        for member in elem._GetActiveMembers():
            try:
                participantsList.remove(member._GetFullName())
            except:
                pass
        if not participantsList:
            print "Checking in."
            elem.SendMessage("#checkin")

            for streamer in streamerList:
                h = httplib2.Http(".cache")
                resp, content = h.request(streamerList[streamer], "GET")
                contentObject = content.decode('utf-8')
                data = json.loads(contentObject) 
                if (data['stream']):
                    print streamer + "'s stream is up!"
                    elem.SendMessage(streamer + "'s stream is up!")

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
skypeClient.Attach()

task =TaskThread(print_checkin, members)
task.run()