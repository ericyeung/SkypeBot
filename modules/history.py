import httplib2, json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('log_messages')

def get_log_messages(key, num):
    try:
        limit = 10
        try:
            limit = int(num)
        except:
            pass
        result = table.query(KeyConditionExpression=Key('chat').eq(key),
                             ScanIndexForward=False,
                             Limit=min(10, limit))['Items']
        return True, list(reversed(result))
    except:
        return False, "Error"

def put_log_message(Message):    
    try:
        data = {
            'chat': Message.Chat.Name,
            'handler': Message.Sender.Handle,
            'message': Message.Body.encode('utf-8'),
            'date': int(Message.Timestamp)
        }
        result = table.put_item(Item=data)
        return True, "Success", Message
    except:
        print("ERROR putting message {}".format(Message.Body.encode('utf-8')))
        return False, "Internal error.", ""
        
