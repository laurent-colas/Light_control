


from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
# table = dynamodb.Table('Movies')
# table.delete()

table = dynamodb.create_table(
    TableName='Light_addresses',
    KeySchema=[
        {
            'AttributeName': 'LocationCode',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'Room',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'LocationCode',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'Room',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

print("Table status:", table.table_status)