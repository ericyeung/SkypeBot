import Skype4Py
import threading

def print_checkin(participants):
    for elem in skypeClient.BookmarkedChats:  # Looks in bookmarked chats and returns True if chat is found.
        for member in elem._GetActiveMembers():
            try:
                participants.remove(member._GetFullName())
            except:
                pass
        if not participants:
            print "Checking in."
            elem.SendMessage("#checkin")

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