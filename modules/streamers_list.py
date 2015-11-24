import httplib2, json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('streamers')

STREAM_ENDPOINT = 'https://api.twitch.tv/kraken/streams/'
USERS_ENDPOINT = 'https://api.twitch.tv/kraken/users/'

def addStreamer(streamer):
	for item in table.scan()['Items']:
		if item['name'] == streamer:
			return False, "Channel already on list."
	try:
		resp, content = httplib2.Http().request(USERS_ENDPOINT + streamer.lower(), "GET")
		contentObject = content.decode('utf-8')
		data = json.loads(contentObject)
		if "error" not in data:
			del data['bio']
			del data['logo']
			data['stream'] = STREAM_ENDPOINT + data['name']
			table.put_item(Item=data)
			return True, "Success", data['display_name']
		else:
			return False, "Channel does not exist."
	except:
		return False, "Internal error."


def removeStreamer(streamer):
	for item in table.scan()['Items']:
		if item['name'] == streamer:
			table.delete_item(Key={'_id': item['_id']})
		return True
	return False

def getStreamers():
	return table.scan()['Items']
