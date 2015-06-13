import httplib2, json

endpoint = 'https://api.twitch.tv/kraken/streams/'


def addStreamer(streamer):
	if streamer.lower() in streamerList:
		return False, "Streamer is already on the list."
	h = httplib2.Http()
	resp, content = h.request(endpoint + streamer,  "GET")
	try:
		contentObject = content.decode('utf-8')
		data = json.loads(contentObject) 
		if ("stream" in data):
			streamerList[streamer] = 'https://api.twitch.tv/kraken/streams/' + streamer
			saveList()
			return True, "Success"
		else:
			return False, "Channel does not exist."
	except:
		pass

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

for line in open('streamers.txt'):
	line = line.strip()
	if line:
		streamerList[line.lower()] = endpoint + line
