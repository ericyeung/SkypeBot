import httplib2, json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('log_messages')

def get_log_messages(num):
    try:
        result = sorted(list(table.scan()['Items']), key=lambda x: x['date'])
        limit = 10
        try:
            limit = int(num)
        except:
            pass
        return True, result[-min(10, limit, len(result)):]
    except:
        return False, "Error"

def put_log_message(Message):
    try:
        data = {
            'handler': Message.Sender.Handle,
            'message': Message.Body.encode('utf-8'),
            'date': int(Message.Timestamp)
        }
        result = table.put_item(Item=data)
        return True, "Success", Message
    except:
        print("ERROR putting message {}".format(Message.Body.encode('utf-8')))
        return False, "Internal error.", ""
        
