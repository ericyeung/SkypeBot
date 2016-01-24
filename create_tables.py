import boto3

dynamodb = boto3.resource('dynamodb')



table = dynamodb.create_table(
    TableName='log_messages',
    KeySchema=[
        {
            'AttributeName': 'chat',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'date',
            'KeyType': 'RANGE'  #Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'chat',
            'AttributeType': 'S'  #Partition key
        },
        {
            'AttributeName': 'date',
            'AttributeType': 'N'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

print("Table status:", table.table_status)
