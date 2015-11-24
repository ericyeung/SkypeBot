import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('skypecheckin')

def getMessage():
    return table.get_item(Key={'type':'message'})['Item']['value']

def updateMessage(message):
    try:
        table.put_item(Item={'type':'message', 'value': message, 'date': datetime.now().strftime("%Y-%m-%d %H:%M %Z")})
        return getMessage()
    except:
        return False
    