import json
import boto3

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # TODO implement
    #print(str(event))
    bucket=event['Records'][0]['s3']['bucket']['name'] #fetch bucket name
    json_file_name=event['Records'][0]['s3']['object']['key'] #fetch file name
    # print(bucket)
    # print(json_file_name)
    json_obj=s3_client.get_object(Bucket=bucket,Key=json_file_name)
    jsonFileReader = json_obj['Body'].read()
    jsonDict = json.loads(jsonFileReader)
    table = dynamodb.Table('Employee')
    table.put_item(Item=jsonDict)
    return "hello from lambda"