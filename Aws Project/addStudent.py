#CODE FOR BOTH DYNAMODB AND S3
import json
import boto3
import time

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
table = dynamodb.Table('StudentTable')

def lambda_handler(event, context):
    d1 = table.scan()
    count = str(d1['Count']+1)
    if "roll_no" in event:
      table.put_item(Item=event)
      json_data = event
    else:
      upd={"roll_no":count}
      upd.update(event)
      table.put_item(Item=upd)
      json_data = upd
    
    bucket_name = 'studentdatabasebucket'
    time_stamp= str(int(time.time()))
    file_name = time_stamp+'.json'
      
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json.dumps(json_data)
    )
    
    return {"code":200, "message":"Student Added Successfull"}



