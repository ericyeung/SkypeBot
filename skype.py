#!/usr/bin/python
import Skype4Py
import threading
import os, time, httplib2, json
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

shop = {'Stimpack': 500,
	'Terrible_Shotgun':5000,
	'Hunting_Rifle':8000,
	'Plasma_Rifle':13000,
	'MIRV':20000, 
	'Black_People_Pesticide': 50000,
	'Vault101': 3000, 
	'Leather': 6000, 
	'Metal': 9000, 
	'Combat': 12000, 
	'Power': 15000} 

death_phrases = ["got killed by Secret Paladin.",
	"got mauled by a deathclaw.",
	"got beaten by a little girl.",
	"accidently fell into a hole.",
	"forgot how to eat and starved to death.", 
	"walked into the wrong neighbourhood.",
	"died of dysentery.", 
	"took an arrow to the knee xD xD xD MEMES xD xD xD.", 
	"committed sudoku"]

bottlecaps = {'dragonslayer965': 1000, 
	'irlightbrite': 1000, 
	'akumaluffy':1500, 
	'windaskk':1000, 
	'elesevd':1000, 
	'ericirq.yeung':1000, 
	'live:biscuitsbot':0, 
	'markpjin':1000, 
	'daskbot':0, 
	'karikenji':1000}

health = {'dragonslayer965': 100, 
	'irlightbrite': 100, 
	'akumaluffy':100, 
	'windaskk':100, 
	'elesevd':100, 
	'ericirq.yeung':100, 
	'live:biscuitsbot': 100, 
	'markpjin':100, 
	'daskbot':100, 
	'karikenji':1000}

armour = {'dragonslayer965': 0, 
	'irlightbrite': 0, 
	'akumaluffy': 0, 
	'windaskk': 0, 
	'elesevd': 0, 
	'ericirq.yeung': 0, 
	'live:biscuitsbot': 0, 
	'markpjin':0, 
	'daskbot':0, 
	'karikenji':0}

weapon = {'dragonslayer965': 0, 
	'irlightbrite': 0, 
	'akumaluffy': 0, 
	'windaskk': 0, 
	'elesevd': 0, 
	'ericirq.yeung': 0, 
	'live:biscuitsbot': 0, 
	'markpjin':0, 
	'daskbot':0, 
	'karikenji':0}

stimpack = {'dragonslayer965': 1, 
	'irlightbrite': 1, 
	'akumaluffy': 1, 
	'windaskk': 1, 
	'elesevd': 1, 
	'ericirq.yeung': 1, 
	'live:biscuitsbot': 1, 
	'markpjin':1, 
	'daskbot':1, 
	'karikenji':1}

bankdebt = {'dragonslayer965': 0, 
	'irlightbrite': 0, 
	'akumaluffy': 0, 
	'windaskk': 0, 
	'elesevd': 0, 
	'ericirq.yeung': 0, 
	'live:biscuitsbot': 0, 
	'markpjin':0, 
	'daskbot':0, 
	'karikenji':0}

energy = {'dragonslayer965': 0, 
	'irlightbrite': 0, 
	'akumaluffy': 0, 
	'windaskk': 0, 
	'elesevd': 0, 
	'ericirq.yeung': 0, 
	'live:biscuitsbot': 0, 
	'markpjin':0, 
	'daskbot':0, 
	'karikenji':0}

chatlog = []
chatlogsenders = []

def commands(Message, Status):

    if Status == 'SENT' or (Status == 'RECEIVED'):
        msg = Message.Body.lower()
        body = Message.Body
        MSH = Message.Sender.Handle
        
        if energy[MSH] <= 19:
            energy[MSH] += 1

       	else:
       	    pass

        if (body.startswith("#") or body.startswith("%") or MSH == "daskbot" or MSH == "live:biscuitsbot"):
            pass       

        else:
            chatlog.append(str(body))
            chatlogsenders.append(str(MSH)) 

        if body.startswith("#chatlog"):         
            splitMessage = body.strip().split(" ")
            history = int(splitMessage[1])
           
            if (history < len(chatlog) and history <= 30):
                chatlogcut = chatlog[-history:]
                chatlogsenders1 = chatlogsenders[-history:]
                Message.Chat.SendMessage("Going back to the last " + str(history) + " message(s).")
                
                for i in range(len(chatlogcut)):
                    Message.Chat.SendMessage(chatlogsenders1[i] + ":" + chatlogcut[i])
           
            else:
                Message.Chat.SendMessage("Buy biscuitsbot premium to get older history!")

        elif (body.startswith("#clearchatlog") and MSH == "ericirq.yeung"):
            del chatlog[:]
            del chatlogsenders[:]
            Message.Chat.SendMessage("Messages deleted.")

        elif body == "#help":
            cmd_help(Message)
        
        elif body.startswith("#patch"):            
            Message.Chat.SendMessage("Visit https://github.com/ericyeung/SkypeBot/blob/master/README.md#todo-list")
          
        elif body.startswith("#tldr"):            
            cmd_tldr(Message)

        elif (body.startswith("#sleep") and MSH == "ericirq.yeung"):
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
        
        elif body.startswith("#explore"):
            if energy[MSH] >= 4:
	            energy[MSH] -= 4  
	            Message.Chat.SendMessage(MSH + " started exploring (-5 energy)!")
	            tempz = rand.randrange(1, 101)
	            Message.Chat.SendMessage(MSH + " rolled a " + str(tempz) + "+" + str(weapon[MSH]) + ".")
	            healthlost = (100-tempz)*(20 - armour[MSH])/20
	         
	            if tempz + weapon[MSH] <= 70:
	                health[MSH] -= healthlost
	                Message.Chat.SendMessage(MSH + " got injured! Lost " + str(healthlost) + " health.")
	            
	                if health[MSH] <= 0:
	                    health[MSH] = 50
	                    
                            if bottlecaps[MSH] > 0:
		                bottlecaps[MSH] /= 2  
		                #Message.Chat.SendMessage(MSH + " has died! You lost half of your bottlecaps.") 
		                Message.Chat.SendMessage(MSH + " " + rand.choice(death_phrases) + "\nYou lost half of your bottlecaps.") 
		            else:
		                bottlecaps[MSH] -= 50
                                Message.Chat.SendMessage(MSH + " " + rand.choice(death_phrases) + "\nYou lost 50 bottlecaps.") 

	            else:
	                bottlecaps[MSH] += tempz*7
	                Message.Chat.SendMessage("Found " + str(tempz*7) + " bottlecaps! (always lucky)")            

	    else:
                Message.Chat.SendMessage("You're too tired! Have some rest.")

        elif body.startswith("#shop") or body.startswith("#store"):
            Message.Chat.SendMessage("Stimpack: 500 \nTerrible_Shotgun: 5000 \nHunting_Rifle: 50000 \nPlasma_Rifle: 50000 \nMIRV: 50000 \nBlack_People_Pesticide: 500000 \nVault101: 3000 \nLeather: 6000 \nMetal: 9000 \nCombat: 12000 \nPower: 15000")
           
        elif body.startswith("#stats"):
            Message.Chat.SendMessage("You have " + str(health[MSH]) + " health.")    
            Message.Chat.SendMessage("You have " + str(armour[MSH]) + " armour.")    
            Message.Chat.SendMessage("You have " + str(weapon[MSH]) + " attack.")    
            Message.Chat.SendMessage("You have " + str(bottlecaps[MSH]) + " bottlecaps.")    
            Message.Chat.SendMessage("You have " + str(stimpack[MSH]) + " stimpacks.")    
            Message.Chat.SendMessage("You have " + str(energy[MSH]) + " energy.")    

        elif body.startswith("#buy"):
            splitMessage = body.strip().split(" ")
            item = splitMessage[1]
            if (bottlecaps[MSH] - shop[item]) <= 0:
                Message.Chat.SendMessage("You don't have enough bottlecaps!")

            else:  
                bottlecaps[MSH] -= shop[item]                
                
                if (item == "Stimpack"):
                    if stimpack[MSH] <= 10:
                    	stimpack[MSH] += 1
                    	Message.Chat.SendMessage("You now have a " + item + "!") 
    	            else:
    			Message.Chat.SendMessage("You can only have 10 stimpacks at a time.") 	

                elif (item == "Terrible_Shotgun"):
                    weapon[MSH] = 3
                    Message.Chat.SendMessage("You now have a " + item + "(3 attack)!")    
              
                elif (item == "Hunting_Rifle"):
                    weapon[MSH] = 6
                    Message.Chat.SendMessage("You now have a " + item + "(6 attack)!")    
                
                elif (item == "Plasma_Rifle"):
                    weapon[MSH] = 9
                    Message.Chat.SendMessage("You now have a " + item + "(9 attack)!")    
              
                elif (item == "MIRV"):
                    weapon[MSH] = 12 
                    Message.Chat.SendMessage("You now have a " + item + "(12 attack)!")                         

                elif (item == "Black_People_Pesticide"):
                    weapon[MSH] = 20 
                    Message.Chat.SendMessage("You now have a " + item + "(20 attack)!")     

                elif (item == "Vault101"):
                    armour[MSH] = 3
                    Message.Chat.SendMessage("You now have a " + item + "(3 armour)!")     

                elif (item == "Leather"):
                    armour[MSH] = 6
                    Message.Chat.SendMessage("You now have a " + item + "(6 armour)!")     

                elif (item == "Metal"):
                    armour[MSH] = 9
                    Message.Chat.SendMessage("You now have a " + item + "(9 armour)!")     

                elif (item == "Combat"):
                    armour[MSH] = 12
                    Message.Chat.SendMessage("You now have a " + item + "(12 armour)!")     

                elif (item == "Power"):
                    armour[MSH] = 15
                    Message.Chat.SendMessage("You now have a " + item + "(15 armour)!")     
        
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
            Message.Chat.SendMessage("Here are the leaderboards!")
            Message.Chat.SendMessage(sorting)

        elif body.startswith("#debug") and MSH == "ericirq.yeung":
            Message.Chat.SendMessage("HEALTH")
            Message.Chat.SendMessage(health)
            Message.Chat.SendMessage("ARMOUR")
            Message.Chat.SendMessage(armour)
            Message.Chat.SendMessage("WEAPON")
            Message.Chat.SendMessage(weapon)
            Message.Chat.SendMessage("BANKDEBT")
            Message.Chat.SendMessage(bankdebt)
	    Message.Chat.SendMessage("ENERGY")
            Message.Chat.SendMessage(energy)

        elif body.startswith("#give") and (MSH == "ericirq.yeung"):
            splitMessage = body.strip().split(" ")
            person = splitMessage[1]
            amount = splitMessage[2]
            bottlecaps[person] = bottlecaps[person] + int(amount)

        else:
            pass
    else:
        pass

def cmd_help(Message):
    Message.Chat.SendMessage('>> #tldr for article summarys')
    Message.Chat.SendMessage('>> #chatlog <#> to go back # messages')
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
