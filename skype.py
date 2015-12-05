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
bottlecaps = {'dragonslayer965': 100, 'irlightbrite': 100, 'akumaluffy':340, 'windaskk':100, 'elesevd':920, 'ericirq.yeung':300, 'live:biscuitsbot': 100}
 
health = {'dragonslayer965': 100, 'irlightbrite': 100, 'akumaluffy':100, 'windaskk':100, 'elesevd':100, 'ericirq.yeung':100, 'live:biscuitsbot': 100}
 
armour = {'dragonslayer965': 0, 'irlightbrite': 0, 'akumaluffy': 0, 'windaskk': 0, 'elesevd': 0, 'ericirq.yeung': 0, 'live:biscuitsbot': 100}
 
weapon = {'dragonslayer965': 0, 'irlightbrite': 0, 'akumaluffy': 0, 'windaskk': 0, 'elesevd': 0, 'ericirq.yeung': 0, 'live:biscuitsbot': 0}
 
stimpack = {'dragonslayer965': 1, 'irlightbrite': 1, 'akumaluffy':1, 'windaskk':1, 'elesevd':1, 'ericirq.yeung':1, 'live:biscuitsbot': 0}
 
shop = {'stimpack': 400, 'Terrible_Shotgun':5000, 'MIRV':50000, 'Vault101_Suit': 2500 , 'Power_Armour': 10000, 'Black_People_Pesticide': 500000}
 
def commands(Message, Status):
 
    if Status == 'SENT' or (Status == 'RECEIVED'):
        msg = Message.Body.lower()
        body = Message.Body
        bottlecaps[Message.Sender.Handle] = bottlecaps[Message.Sender.Handle] + 10
 
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
            Message.Chat.SendMessage(">> Thanks for checking in, " + Message.Sender.Handle + "!")
 
        elif body.startswith("#checkout"):
            Message.Chat.SendMessage(">> Bye " + Message.Sender.Handle + "!")
 
        elif body.startswith("Moji"):
            Message.Chat.SendMessage("EMOJI DETECTED")
 
        elif body.startswith("#bottlecap"):
            Message.Chat.SendMessage(Message.Sender.Handle + ", you have " + str(bottlecaps[Message.Sender.Handle]) + " bottlecaps!")
       
        elif body.startswith("#explore"):
            Message.Chat.SendMessage("You started exploring!")
            tempz = rand.randrange(1, 51)
            Message.Chat.SendMessage("You rolled a " + str(tempz) + " .")
 
            if tempz + weapon[Message.Sender.Handle] <= 30:
                health[Message.Sender.Handle] = health[Message.Sender.Handle] - 20
                Message.Chat.SendMessage("You got injured! Lost 20 health.")
           
                if health[Message.Sender.Handle] <= 0:
                    bottlecaps[Message.Sender.Handle] = bottlecaps[Message.Sender.Handle]/2  
                    Message.Chat.SendMessage("You have died! Lost half of your bottlecaps.")
                    health[Message.Sender.Handle] = health[Message.Sender.Handle] + 60
 
            else:
                bottlecaps[Message.Sender.Handle] = bottlecaps[Message.Sender.Handle] + tempz*10
                Message.Chat.SendMessage("Found " + str(tempz*10) + " bottlecaps! (always lucky)")            
 
        elif body.startswith("#shop"):
            Message.Chat.SendMessage("Stimpack: 100 \nTerrible_Shotgun: 500 \nMIRV: 1000 \nVault101_Suit \nPower_Armour: 10000 \nBlack_People_Pesticide: 50000")
           
        elif body.startswith("#stats"):
            Message.Chat.SendMessage("You have " + str(health[Message.Sender.Handle]) + " health.")    
            Message.Chat.SendMessage("You have " + str(weapon[Message.Sender.Handle]) + " attack.")    
 
        elif body.startswith("#buy"):
            splitMessage = body.strip().split(" ")
            item = splitMessage[1]
            if (bottlecaps[Message.Sender.Handle] - shop[item]) <= 0:
                Message.Chat.SendMessage("You don't have enough bottlecaps!")
 
            else:  
                bottlecaps[Message.Sender.Handle] = bottlecaps[Message.Sender.Handle] - shop[item]                
               
                if (item == "stimpack"):
                    stimpack[Message.Sender.Handle] = stimpack[Message.Sender.Handle] + 1
                    Message.Chat.SendMessage("You now have a " + item + "!")
               
                elif (item == "Terrible_Shotgun"):
                    weapon[Message.Sender.Handle] = weapon[Message.Sender.Handle] + 1
                    Message.Chat.SendMessage("You now have a " + item + "!")    
             
                elif (item == "MIRV"):
                    weapon[Message.Sender.Handle] = weapon[Message.Sender.Handle] + 5
                    Message.Chat.SendMessage("You now have a " + item + "!")                        
 
                elif (item == "Black_People_Pesticide"):
                    weapon[Message.Sender.Handle] = weapon[Message.Sender.Handle] + 10
                    Message.Chat.SendMessage("You now have a " + item + "!")    
 
                elif (item == "Vault101_Suit"):
                    health[Message.Sender.Handle] = health[Message.Sender.Handle] + 10
                    armour[Message.Sender.Handle] = armour[Message.Sender.Handle] + 10
                    Message.Chat.SendMessage("You now have a " + item + "!")    
 
                elif (item == "Power_Armour"):
                    health[Message.Sender.Handle] = health[Message.Sender.Handle] + 50
                    armour[Message.Sender.Handle] = armour[Message.Sender.Handle] + 50
                    Message.Chat.SendMessage("You now have a " + item + "!")    
       
        elif body.startswith("#deathclaw"):
            Message.Chat.SendMessage("First turn, deathclaw attacks first!")
            tempx = rand.randrange(1, 101)
            if tempx + armour[Message.Sender.Handle] <= 51:
                health[Message.Sender.Handle] = health[Message.Sender.Handle] - 50
                Message.Chat.SendMessage("You're crippled! Lost 50 health.")
               
        elif body.startswith("#heal"):
            if stimpack[Message.Sender.Handle] > 0:
                health[Message.Sender.Handle] = health[Message.Sender.Handle] + 50
                stimpack[Message.Sender.Handle] = stimpack[Message.Sender.Handle] - 1
                Message.Chat.SendMessage("Restored 50 health. \n" + str(stimpack[Message.Sender.Handle]) + " stimpacks left.")
            else:
                Message.Chat.SendMessage("No stimpacks! Buy one from the store.")
 
        elif body.startswith("#leaderboard"):
            sorting = sorted(bottlecaps.items(), key = lambda x: x[1], reverse = True)
            print sorting
            Message.Chat.SendMessage(sorting)
 
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
    Message.Chat.SendMessage('>> #health to check your health')
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
 
if __name__ == "__main__":
    main()
