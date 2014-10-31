import Skype4Py
import threading

def print_checkin():
	for elem in skypeClient.BookmarkedChats:  # Looks in bookmarked chats and returns True if chat is found.
		if len(elem.Members) > 2 and (member.Handler == "irlightbrite" for member in elem.Members): #Make Sure Clarence is in the chat
			print "Checking in."
			elem.SendMessage("#checkin")


class TaskThread(threading.Thread):
    """Thread that executes a task every N seconds"""
    
    def __init__(self, task):
        threading.Thread.__init__(self)
        self._finished = threading.Event()
        self._interval = 3600
        self.task = task
    
    def setInterval(self, interval):
        """Set the number of seconds we sleep between executing our task"""
        self._interval = interval
    
    def run(self):
        while 1:
            if self._finished.isSet(): return
            self.task()

            self._finished.wait(self._interval)


# Create an instance of the Skype class.
skypeClient = Skype4Py.Skype()
skypeClient.Attach()

task =TaskThread(print_checkin)
task.run()