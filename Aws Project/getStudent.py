import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentTable')

def lambda_handler(event, context):
    roll_no = event['roll_no']
    resp = table.get_item(Key={
        "roll_no":roll_no
    })
    return resp['Item']
