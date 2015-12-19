#!/usr/bin/python
from __future__ import division
import Skype4Py
import threading
import httplib2, json
import os, time
import random as rand
from tldr import cmd_tldr
from allotrope import allotrope
from buy import buy
from helplist import cmd_help 

def print_checkin(participants):

    for elem in skypeClient.BookmarkedChats:  # Looks in bookmarked chats and returns True if chat is found.
        participantsList = list(participants)
        for member in elem._GetActiveMembers():
            try:
                participantsList.remove(member._GetFullName())
            except:
                pass
        if not participantsList:
            #print "Checking in."
            #print (time.strftime("%H:%M:%S")) # timestamps for checkins

bottlecaps = {'dragonslayer965': 8385, 'irlightbrite': 6610, 'akumaluffy':2995, 'windaskk':6270, 'elesevd':3748, 'ericirq.yeung':1425, 'live:biscuitsbot': 5145}

health = {'dragonslayer965': 100, 'irlightbrite': 100, 'akumaluffy':100, 'windaskk':100, 'elesevd':100, 'ericirq.yeung':100, 'live:biscuitsbot': 100}

armour = {'dragonslayer965': 0, 'irlightbrite': 15, 'akumaluffy': 3, 'windaskk': 0, 'elesevd': 3, 'ericirq.yeung': 3, 'live:biscuitsbot': 100}

weapon = {'dragonslayer965': 0, 'irlightbrite': 0, 'akumaluffy': 0, 'windaskk': 0, 'elesevd': 10, 'ericirq.yeung': 0, 'live:biscuitsbot': 0}

stimpack = {'dragonslayer965': 1, 'irlightbrite': 1, 'akumaluffy':1, 'windaskk':1, 'elesevd':1, 'ericirq.yeung':1, 'live:biscuitsbot': 0}

shop = {'stimpack': 500, 'Terrible_Shotgun':5000, 'MIRV':50000, 'Vault101': 2500 , 'Leather': 5000, 'Metal': 7500, 'Combat': 10000, 'Power': 12500, 'Black_People_Pesticide': 500000}

bankdebt = {'dragonslayer965': 0, 'irlightbrite': 0, 'akumaluffy':0, 'windaskk':0, 'elesevd':0, 'ericirq.yeung':0, 'live:biscuitsbot': 0}

def commands(Message, Status):

    if Status == 'SENT' or (Status == 'RECEIVED'):
        msg = Message.Body.lower()
        body = Message.Body
        MSH = Message.Sender.Handle
        bottlecaps[MSH] += 5
        bannedlist = []        

        elif body == "#help":
            cmd_help(Message)
        
        elif body.startswith("#tldr"):            
            cmd_tldr(Message)

        elif body.startswith("#allotrope"):            
            allotrope(Message)

        elif body.startswith("#sleep"):
            splitMessage = body.strip().split(" ")
            sleeptime = splitMessage[1]
            sleepint = int(float(sleeptime))
            Message.Chat.SendMessage('>> Sleeping... for' + sleepint + 'minutes')
            time.sleep(sleepint) # seconds 
            print "Script paused..."
            Message.Chat.SendMessage('>> BiscuitsBot is awake!')
            print "Script resumed."

        elif body.startswith("#killbot"):
            splitMessage = body.strip().split(" ") # splits the message into command and argument
            secretpassword = splitMessage[1]
            if secretpassword == ("kappa123"):
                Message.Chat.SendMessage('>> Correct password, goodbye!')
                #os._exit(0)
                Message.Chat.SendMessage('>> JUST KIDDING') 
            else: 
                Message.Chat.SendMessage('>> WRONG PASSWORD, UNABLE TO TERMINATE')

        elif body.startswith("#checkin") and Status == "RECEIVED": 
            Message.Chat.SendMessage(">> Thanks for checking in, " + MSH + "!") 

        elif body.startswith("#checkout"):
            Message.Chat.SendMessage(">> Bye " + MSH + "!")

        elif body.startswith("Moji"):
            Message.Chat.SendMessage("EMOJI DETECTED")

        elif body.startswith("#bottlecap"):
            Message.Chat.SendMessage(MSH + ", you have " + str(bottlecaps[MSH]) + " bottlecaps!")
        
        elif body.startswith("#explore") and (str(MSH) not in bannedlist):
            
            if (bottlecaps[MSH] - 25) <= 0:
                Message.Chat.SendMessage("You don't have enough bottlecaps!")

            else:    
                bottlecaps[MSH] -= 25  
                bottlecaps[ericirq.yeung] += 25
                Message.Chat.SendMessage(MSH + " started exploring (-25 bottlecaps)!")
                tempz = rand.randrange(1, 101)
                Message.Chat.SendMessage(MSH + " rolled a " + str(tempz) + ".")
                healthlost = tempz*(20 - armour[MSH])/20

                if tempz + weapon[MSH] <= 70:
                    health[MSH] -= healthlost
                    Message.Chat.SendMessage(MSH + " got injured! Lost " + str(healthlost) + " health.")
                
                    if health[MSH] <= 0:
                        bottlecaps[MSH] /= 2  
                        Message.Chat.SendMessage(MSH + " has died! You lost half of your bottlecaps.") 
                        health[MSH] = 50

                else:
                    bottlecaps[MSH] += tempz*7
                    Message.Chat.SendMessage("Found " + str(tempz*7) + " bottlecaps! (always lucky)")           

        elif body.startswith("#shop") or body.startswith("#store"):
            Message.Chat.SendMessage("Stimpack: 500 \nTerrible_Shotgun: 5000 \nMIRV: 50000 \nBlack_People_Pesticide: 500000 \nVault101: 2500 \nLeather: 5000 \nMetal: 7500 \nCombat: 10000 \nPower: 12500")
        
        elif body.startswith("#bank"):
            Message.Chat.SendMessage("Welcome to the Iron Bank of Braavos!")
            Message.Chat.SendMessage("Type #getloan <amount> to get a loan!")
            Message.Chat.SendMessage("Type #payloan <amount> to pay back your debt!")
            Message.Chat.SendMessage("If you are >2000 bottlecaps in debt, we will fund your enemies.")

        elif body.startswith("#getloan"):
            splitMessage = body.strip().split(" ")
            loanamount = splitMessage[1]

            if loanamount <= 2000 and bankdebt[MSH] <= 2000: 
                bottlecaps[MSH] += loanamount
                bankdebt[MSH] += loanamount
                Message.Chat.SendMessage(MSH + "borrowed " + str(loanamount) + " bottlecaps.")    

            else:
                Message.Chat.SendMessage("You are trying to borrow too much.")    

        elif body.startswith("#payloan"):
            splitMessage = body.strip().split(" ")
            payback = splitMessage[1]
            bankdebt[MSH] -= payback
            bottlecaps[ericirq.yeung] += payback
            Message.Chat.SendMessage(MSH + "paid back " + str(payback) + " bottlecaps.")    

        elif body.startswith("#stats"):
            Message.Chat.SendMessage("You have " + str(health[MSH]) + " health.")    
            Message.Chat.SendMessage("You have " + str(armour[MSH]) + " armour.")    
            Message.Chat.SendMessage("You have " + str(weapon[MSH]) + " attack.")    

        elif body.startswith("#buy"):
            buy(Message)

        elif body.startswith("#heal"):
            if stimpack[MSH] > 0:
                health[MSH] = health[MSH] + 50
                
                if health[MSH] > 100:
                    health[MSH] = 100        

                stimpack[MSH] = stimpack[MSH] - 1
                Message.Chat.SendMessage("Restored 50 health. \n" + str(stimpack[MSH]) + " stimpacks left.")
            else:
                Message.Chat.SendMessage("No stimpacks! Buy one from the store.")

        elif body.startswith("#leaderboard"):
            sorting = sorted(bottlecaps.items(), key = lambda x: x[1], reverse = True)
            print sorting
            Message.Chat.SendMessage(sorting)

        elif body.startswith("#debug") and MSH == "ericirq.yeung":
            Message.Chat.SendMessage(health)
            Message.Chat.SendMessage(armour)
            Message.Chat.SendMessage(weapon)

        elif body.startswith("#give") and (MSH == "ericirq.yeung" or MSH == "irlightbrite"):
            splitMessage = body.strip().split(" ")
            person = splitMessage[1]
            amount = splitMessage[2]
            bottlecaps[person] = bottlecaps[person] + int(amount)

        elif body.startswith("#ban") and (MSH == "ericirq.yeung" or MSH == "irlightbrite"):
            splitMessage = body.strip().split(" ")
            person = str(splitMessage[1])
            bannedlist.append(person)
            print bannedlist

        else:
            pass
    else:
        pass

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
