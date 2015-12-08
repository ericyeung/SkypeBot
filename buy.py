def buy(Message):
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
            weapon[MSH] = 5 # Removed Dual Wield
            Message.Chat.SendMessage("You now have a " + item + "(5 attack)!")    
      
        elif (item == "MIRV"):
            weapon[MSH] = 10 
            Message.Chat.SendMessage("You now have a " + item + "(10 attack)!")                         

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
