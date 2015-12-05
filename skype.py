#!/usr/bin/python
import Skype4Py
import threading
import httplib2, json
import os, time
import random as rand
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
            #elem.SendMessage("#checkin")
            #elem.SendMessage(">> I am BiscuitsBot")

# Initial currency (should have a file to r/w)
bottlecaps = {'dragonslayer965': 500, 'irlightbrite': 500, 'akumaluffy':500, 'windaskk':500, 'elesevd':500, 'ericirq.yeung':500, 'live:biscuitsbot': 100}

health = {'dragonslayer965': 100, 'irlightbrite': 100, 'akumaluffy':100, 'windaskk':100, 'elesevd':100, 'ericirq.yeung':100, 'live:biscuitsbot': 100}

armour = {'dragonslayer965': 0, 'irlightbrite': 0, 'akumaluffy': 0, 'windaskk': 0, 'elesevd': 0, 'ericirq.yeung': 0, 'live:biscuitsbot': 100}

weapon = {'dragonslayer965': 0, 'irlightbrite': 0, 'akumaluffy': 0, 'windaskk': 0, 'elesevd': 0, 'ericirq.yeung': 0, 'live:biscuitsbot': 0}

stimpack = {'dragonslayer965': 1, 'irlightbrite': 1, 'akumaluffy':1, 'windaskk':1, 'elesevd':1, 'ericirq.yeung':1, 'live:biscuitsbot': 0}

shop = {'stimpack': 500, 'Terrible_Shotgun':5000, 'MIRV':50000, 'Vault101_Suit': 2500 , 'Power_Armour': 10000, 'Black_People_Pesticide': 500000}

def commands(Message, Status):

    if Status == 'SENT' or (Status == 'RECEIVED'):
        msg = Message.Body.lower()
        body = Message.Body
        MSH = Message.Sender.Handle
        bottlecaps[MSH] += 10
        bannedlist = []        
        healthlost = 20 - armour[MSH]

        if body == "#beep":
            cmd_test(Message)
        
        elif body == "#poll":
            cmd_poll(Message)

        elif body == "#help":
            cmd_help(Message)
        
        elif body.startswith("#tldr"):            
            cmd_tldr(Message)

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

        elif body.startswith("#call"):
            #GetCallWith()
            Message.Chat.SendMessage('>> Sorry! This feature is not yet available.')

        elif body.startswith("#checkin") and Status == "RECEIVED": 
            Message.Chat.SendMessage(">> Thanks for checking in, " + MSH + "!") 

        elif body.startswith("#checkout"):
            Message.Chat.SendMessage(">> Bye " + MSH + "!")

        elif body.startswith("Moji"):
            Message.Chat.SendMessage("EMOJI DETECTED")

        elif body.startswith("#bottlecap"):
            Message.Chat.SendMessage(MSH + ", you have " + str(bottlecaps[MSH]) + " bottlecaps!")
        
        elif body.startswith("#explore") and (str(MSH) not in bannedlist):
            bottlecaps[MSH] -= 50  
            Message.Chat.SendMessage(MSH + " started exploring (-50 bottlecaps)!")
            tempz = rand.randrange(1, 51)
            Message.Chat.SendMessage(MSH + " rolled a " + str(tempz) + ".")

            if tempz + weapon[MSH] <= 35:
                health[MSH] -= healthlost
                Message.Chat.SendMessage(MSH + " got injured! Lost " + str(healthlost) + " health.")
            
                if health[MSH] <= 0:
                    bottlecaps[MSH] /= 2  
                    Message.Chat.SendMessage(MSH + " has died! You lost half of your bottlecaps.") 
                    health[MSH] = 50

            else:
                bottlecaps[MSH] += tempz*5
                Message.Chat.SendMessage("Found " + str(tempz*5) + " bottlecaps! (always lucky)")            

        elif body.startswith("#shop"):
            Message.Chat.SendMessage("Stimpack: 500 \nTerrible_Shotgun: 5000 \nMIRV: 50000 \nVault101_Suit: 2500 \nPower_Armour: 10000 \nBlack_People_Pesticide: 500000")
           
        elif body.startswith("#stats"):
            Message.Chat.SendMessage("You have " + str(health[MSH]) + " health.")    
            Message.Chat.SendMessage("You have " + str(weapon[MSH]) + " attack.")    

        elif body.startswith("#buy"):
            splitMessage = body.strip().split(" ")
            item = splitMessage[1]
            if (bottlecaps[MSH] - shop[item]) <= 0:
                Message.Chat.SendMessage("You don't have enough bottlecaps!")

            else:  
                bottlecaps[MSH] -= shop[item]                
                
                if (item == "stimpack"):
                    stimpack[MSH] += 1
                    Message.Chat.SendMessage("You now have a " + item + "!") 
                
                elif (item == "Terrible_Shotgun"):
                    weapon[MSH] += 5
                    Message.Chat.SendMessage("You now have a " + item + "(5 attack)!")    
              
                elif (item == "MIRV"):
                    weapon[MSH] += 10 
                    Message.Chat.SendMessage("You now have a " + item + "(10 attack)!")                         

                elif (item == "Black_People_Pessticide"):
                    weapon[MSH] += 20 
                    Message.Chat.SendMessage("You now have a " + item + "(20 attack)!")     

                elif (item == "Vault101_Suit"):
                    armour[MSH] += 5
                    Message.Chat.SendMessage("You now have a " + item + "(5 armour)!")     

                elif (item == "Power_Armour"):
                    armour[MSH] += 10
                    Message.Chat.SendMessage("You now have a " + item + "(10 armour)!")     
        
                health[MSH] = health[MSH] - 50

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
            print health; print armour; print weapon

        elif body.startswith("#give") and MSH == "ericirq.yeung":
            splitMessage = body.strip().split(" ")
            person = splitMessage[1]
            amount = splitMessage[2]
            bottlecaps[person] = bottlecaps[person] + int(amount)

        elif body.startswith("#ban") and MSH == "ericirq.yeung":
            splitMessage = body.strip().split(" ")
            person = str(splitMessage[1])
            timeban = float(splitMessage[2])
            bannedlist.append(person)
            print bannedlist
            time.sleep(timeban)
            bannedlist.remove(person)            
            print bannedlist  

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
    Message.Chat.SendMessage('>> #tldr for article summarys')
    Message.Chat.SendMessage('>> #stopbot to put BiscuitsBot to sleep')
    Message.Chat.SendMessage('>> #killbot to murder BiscuitsBot')
    Message.Chat.SendMessage('>> RPG COMMANDS BELOW')
    Message.Chat.SendMessage('>> #bottlecap to check your bottlecap balance. (You get 10 per message)')
    Message.Chat.SendMessage('>> #explore to get potential bottlecaps (40% chance for success)')
    Message.Chat.SendMessage('>> #heal to use a stimpack and regain 50 health')
    Message.Chat.SendMessage('>> #stats to check your health and attack')
    Message.Chat.SendMessage('>> #shop to go shopping')
    Message.Chat.SendMessage('>> #buy to buy stuff')
    Message.Chat.SendMessage('>> #leaderboard to check the bottlecap rankings')

arena_cards = ["first card","second card","third card"]

def getpollanswer():
    return arena_cards[rand.randint(0,2)]

def cmd_poll(Message):
    Message.Chat.SendMessage(">> choose the " + getpollanswer())

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

"""
elif body.startswith("#deathclaw"):
Message.Chat.SendMessage("First turn, deathclaw attacks first!")
tempx = rand.randrange(1, 101)
if tempx + armour[MSH] <= 51:
Message.Chat.SendMessage("You're crippled! Lost 50 health.") 
"""                
