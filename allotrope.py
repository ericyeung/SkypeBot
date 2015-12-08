def allotrope(Message):
    splitMessage = body.strip().split(" ")
    element = splitMessage[1] 

    if element == "Carbon":
        Message.Chat.SendMessage("Diamond – an extremely hard, transparent crystal, with the carbon atoms arranged in a tetrahedral lattice. A poor electrical conductor. An excellent thermal conductor.")
        Message.Chat.SendMessage("Lonsdaleite – also called hexagonal diamond.")
        Message.Chat.SendMessage("Q-carbon – a ferromagnetic, tough, and brilliant crystal structure that is harder and brighter than diamonds.")
        Message.Chat.SendMessage("Graphite – a soft, black, flaky solid, a moderate electrical conductor. The C atoms are bonded in flat hexagonal lattices (graphene), which are then layered in sheets.")
        Message.Chat.SendMessage("Linear acetylenic carbon (Carbyne)")
        Message.Chat.SendMessage("Amorphous carbon")
        Message.Chat.SendMessage("Fullerenes, including Buckminsterfullerene, a.k.a. buckyballs, such as C60.")
        Message.Chat.SendMessage("Carbon nanotubes – allotropes of carbon with a cylindrical nanostructure.")

    elif element == "Oxygen":
        Message.Chat.SendMessage("Dioxygen, O2 – colorless (faint blue)")
        Message.Chat.SendMessage("Ozone, O3 – blue")
        Message.Chat.SendMessage("Tetraoxygen, O4 – metastable")
        Message.Chat.SendMessage("Octaoxygen, O8 – red")

    elif element == "Silicon":
        Message.Chat.SendMessage("Amorphous silicon")
        Message.Chat.SendMessage("crystalline silicon, Diamond cubic structure")

    elif element == "Germanium":        
        Message.Chat.SendMessage("alpha-germanium – semimetallic, with the same structure as diamond")
        Message.Chat.SendMessage("beta-germanium – metallic, with the same structure as beta-tin")
        
    elif element == "Tellurium":    
        Message.Chat.SendMessage("amorphous tellurium - gray-black or brown powder")
        Message.Chat.SendMessage("crystalline tellurium - hexagonal crystalline structure (metalloid)")

    elif element == "Iron":    
        Message.Chat.SendMessage("ferrite (alpha iron): forms below 770 °C (the Curie point, TC); the iron becomes magnetic in its alpha form; BCC crystal structure")
        Message.Chat.SendMessage("beta: forms below 912 °C; BCC crystal structure")
        Message.Chat.SendMessage("gamma: forms below 1,394 °C; FCC crystal structure")
        Message.Chat.SendMessage("delta: forms from cooling down molten iron below 1,538 °C; BCC crystal structure")
        Message.Chat.SendMessage("epsilon: forms at high pressures")
        
    elif element == "Cobalt":
        Message.Chat.SendMessage("alpha-Cobalt – forms above 417 °C simple cubic (metallic)")
        Message.Chat.SendMessage("beta-Cobalt – forms below 417 °C hexagonal close packed (hcp) (metallic)")
        
    elif element == "Polonium":    
        Message.Chat.SendMessage("alpha-polonium – simple cubic (metallic)")
        Message.Chat.SendMessage("beta-polonium – rhombohedral (metallic)")

    else:
        Message.Chat.SendMessage("This element does not have an allotrope.")
    