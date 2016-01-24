import boto3
import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('log_messages')

result = sorted(list(table.scan()['Items']), key=lambda x: x['date'])
for log in result:
    print("{},{},{}".format(datetime.datetime.fromtimestamp(log['date']), log['handler'], log['message'].encode('utf-8').replace(",", '[COMMA]').replace("\n", '').replace('\r', '')))
