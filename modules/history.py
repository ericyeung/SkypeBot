import httplib2, json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('log_messages')

def get_log_messages(chat, num):
    try:
        limit = 10
        try:
            limit = int(num)
        except:
            if num.strip() != '':
                return False, "Error"
        result = table.query(KeyConditionExpression=Key('chat').eq(chat),
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

def query_log_messages_frequency(chat, query):
    try:
        result = table.scan(ScanFilter={'message': { 'AttributeValueList': [ query ], 'ComparisonOperator': 'CONTAINS' }})['Items']
        return True, result
    except:
        return False, "Error"
