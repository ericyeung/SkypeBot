This project is now discontinued since Mircosoft changed how bots behave in chats. May still work with legacy versions of Skype [(<= 7.21)](http://www.skaip.org/skype-7-21-0-100-for-windows-desktop).
==============

Installation
==============

Get 32-bit python and type ```pip install Skype4Py PyTeaser``` into your commandline. You will also need [Python-Goose](https://github.com/grangier/python-goose). 
Clone this repository ```git clone https://github.com/ericyeung/SkypeBot.git```. 
Open Skype and then bookmark the chat you want your bot to operate in. Now run the script ```python skype.py```. Have fun! 

TODO: List
==============
- [x] Put stimpack count and bottlecaps in ```#stats```. 
- [x] Increase number of weapons, fairly distribute the prices. 
- [x] Make it so that the damage taken scales inversely proportional to the roll (i.e., rolling a 1 makes you take more damage then rolling a 69.)
- [ ] Make exploring more skill-based.
- [ ] Raids, bosses, endgame content
- [x] Fix loan stuff
- [ ] Make read/write to store stuff. 
- [x] Clarify debug command. 
- [x] Change exploring cost to "energy".
- [x] 10 Stimpack limit.
- [x] You now lose a flat amount of bottlecaps when you are in the negatives. 
- [ ] Implement PVP and trading system. 
- [x] Removed the Iron Bank of Braavos. 
- [ ] Give every message 5 bottlecaps again?

Usage 
==============

An example of the ```#tldr``` command: 
```
#tldr http://news.utoronto.ca/satoru-iwata-why-generation-mourning-loss-nintendos-ceo
>> Summarizing your article...
Many of their creations featured balloons floating away – a reference to one of the games Iwata helped create.
Since becoming Nintendo's president, he's been the executive producer on countless Nintendo games from the GameCube era and onward.
The impact of Satoru Iwata's death won't be felt as much as that of Steve Jobs, but it will be similar.
These games still inspire me today, since I'm developing video games myself right now.
When I was younger, I was introduced to video games on the computer.
>> The article title is "Satoru Iwata: why a generation is mourning the loss of Nintendo's CEO | U of T News"
```

RPG Bot
==============
Get in-chat currency every time you type! Get bottlecaps to go exploring the wasteland for loot! 
```
#tldr for article summarys
#stopbot to put BiscuitsBot to sleep
#killbot to murder BiscuitsBot
#bottlecap to check your bottlecap balance. (You get 10 per message)
#explore to get potential bottlecaps (40% chance for success)
#heal to use a stimpack and regain 50 health
#stats to check your health and attack
#shop to go shopping
#buy to buy stuff
#leaderboard to check the bottlecap rankings
```

Chat logs
==============
Tired of seeing removed or edited messages? No problem! Type ```!chatlog <# of messages retrieved>``` to get the messages removed/edited. 
