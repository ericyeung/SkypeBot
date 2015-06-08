def addStreamer(streamer):
    streamersList.append(streamer)
    streamerList[streamer] = 'https://api.twitch.tv/kraken/streams/' + streamer

# List of streamers to subscribe to
streamersList = ['Windask','LightBrite','DragonSlayer965', 'Kin_Tsuna', 'iGumdrop', 'OGKhey', 'itsHafu', "AkumaLuffy", "nl_Kripp", "Handmade_Hero", "LoLGeranimo", "BehkuhTV"]
streamerList = {}

for streamer in streamersList:
    streamerList[streamer] = 'https://api.twitch.tv/kraken/streams/' + streamer
