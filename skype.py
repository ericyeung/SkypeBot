#!/usr/bin/python
# -*- coding: <encoding name> -*-
import Skype4Py
import threading
import httplib2, json
import os, time
from tldr import cmd_tldr

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
            print (time.strftime("%H:%M:%S")) # timestamps for checkins
            elem.SendMessage("#checkin")
            elem.SendMessage(">> I am BiscuitsBot")

def commands(Message, Status):
    if Status == 'SENT' or (Status == 'RECEIVED'):
        msg = Message.Body.lower()
        body = Message.Body
        if body == "#beep":
            cmd_test(Message)
        
        elif body == "#poll":
            cmd_poll(Message)

        elif body == "#help":
            cmd_help(Message)
        
        elif body.startswith("#tldr"):            
        	cmd_tldr(Message)

        elif body.startswith("#stopbot"):
            Message.Chat.SendMessage('>> Sleeping... for a while')
            print "Script paused..."
            time.sleep(60.*1.) # 30 = 30 minutes
            Message.Chat.SendMessage('>> BiscuitsBot is awake!')
            print "Script resumed."

        elif body.startswith("#killbot"):
            Message.Chat.SendMessage('>> TOXIC COMMAND, UNABLE TO TERMINATE')
            #os._exit(0)

        elif body.startswith("#call"):
            #GetCallWith()
            Message.Chat.SendMessage('>> Sorry! This feature is not yet available. Please contact Ryan.')

        elif body.startswith("#checkin") and Status == "RECEIVED":
            Message.Chat.SendMessage('>> Hello human/machine, thanks for checking in!') 

        elif body.startswith("#checkout"):
            Message.Chat.SendMessage('>> Bye human!')

        else:
            pass
    else:
        pass

def cmd_test(Message):
    Message.Chat.SendMessage('>> Beep')
    time.sleep(.5)
    Message.Chat.SendMessage('>> Boop')
    time.sleep(.5)
    Message.Chat.SendMessage('>> Beep')
    time.sleep(.5)
    print "Testing complete.\n"

def cmd_help(Message):
    Message.Chat.SendMessage('>> #beep for beep boops')
    Message.Chat.SendMessage('>> #poll for arena help')
    Message.Chat.SendMessage('>> #tldr for article summarys [in progress]')
    Message.Chat.SendMessage('>> #stopbot to put BiscuitsBot to sleep')
    Message.Chat.SendMessage('>> #call for group calls [do not use this yet]')
    Message.Chat.SendMessage('>> #killbot to murder BiscuitsBot')

import random as rand
arena_cards = ["first card","second card","third card"]

def getpollanswer():
    return arena_cards[rand.randint(0,2)]

def cmd_poll(Message):
    Message.Chat.SendMessage(">> choose the" + getpollanswer())

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

skypeClient.OnMessageStatus = commands 

task =TaskThread(print_checkin, members)
task.run()
    
if __name__ == "__main__":
    main()
            
