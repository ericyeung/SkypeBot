import httplib2, json
from files import tryReading

endpoint = 'https://api.twitch.tv/kraken/streams/'

def addStreamer(streamer):
	if streamer.lower() in streamerList:
		return False, "Streamer is already on the list."
	try:
		resp, content = httplib2.Http().request(endpoint + streamer.lower(),  "GET")
		contentObject = content.decode('utf-8')
		data = json.loads(contentObject) 
		if ("stream" in data):
			streamerList[streamer.lower()] = 'https://api.twitch.tv/kraken/streams/' + streamer.lower()
			saveList()
			return True, "Success"
		else:
			return False, "Channel does not exist."
	except:
		return False, "Internal error."

def removeStreamer(streamer):
	if streamer.lower() in streamerList:
		del streamerList[streamer.lower()]
		saveList()
		return True
	return False


def saveList():
	f = open('streamers.txt', 'w')
	for streamer in streamerList:
		f.write(streamer + "\n")

# List of streamers to subscribe to
streamerList = {}



for line in tryReading('streamers.txt'):
	line = line.strip()
	if line:
		streamerList[line.lower()] = endpoint + line
