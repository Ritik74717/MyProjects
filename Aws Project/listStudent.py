import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentTable')

def lambda_handler(event, context):
    data = table.scan()
    l=data['Items']
    return l
    
    
