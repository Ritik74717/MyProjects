import boto3
import json
import pandas as pd
import os


def lambda_handler(event, context):
  # Get the S3 object details from the event
  s3_client = boto3.client('s3')
  bucket = event['Records'][0]['s3']['bucket']['name']
  #print(bucket)
  key = event['Records'][0]['s3']['object']['key']
  #print(key)
  filepath = "/tmp/"+ key
  s3_client.download_file(bucket, key, filepath)
  print("file-downloaded successfully")
  file_path = os.path.join('/tmp', key)
  try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)
        # Convert DataFrame to JSON string with each row as a separate object
        json_data = df.to_json(orient='records', lines=True)
        # Split the JSON string by newline characters to get individual JSON objects
        json_objects = json_data.strip().split('\n')
        # Convert each JSON object to a dictionary and append to a list
        data = [json.loads(obj) for obj in json_objects]
        # Get a DynamoDB resource
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('employeetable')
        #put data into table
        for e in data:
          e['emp_id']=str(e['emp_id'])
          table.put_item(Item=e)
          
  except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        
  return f"Data Uploaded Successfully"
  
  
  

# import json
# import boto3

# s3_client = boto3.client('s3')
# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('Employee')

# def lambda_handler(event, context):
#     # TODO implement
#     bucket=event['Records'][0]['s3']['bucket']['name'] #fetch bucket name
#     print(bucket)
#     s3_file_name=event['Records'][0]['s3']['object']['key'] #fetch file name
#     print(s3_file_name)
#     resp=s3_client.get_object(Bucket=bucket,Key=s3_file_name)
#     data=resp['Body'].read().decode("utf-8")
#     empl=data.split("\n")
#     print(empl)
    
#     for emp in empl:
#         print(emp)
#         empdata=emp.split(",")
#         #put data in dynamodb
#         try:
#              table.put_item(
#               Item={
#                   "emp_id":int(empdata[0]),
#                     "address":empdata[1],
#                     "department":empdata[2],
#                     "emp_name":empdata[3],
#                     "salary":empdata[4]
                   
#               }
#               )
#         except Exception as e:
#             print("End of line")
        
    
#     return "hello from lambda"


