import boto3
from datetime import datetime

# Initialize DynamoDB and SES clients
dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')

def lambda_handler(event, context):
    #Get current date
    current_date = datetime.utcnow().strftime('%m-%d')
    print(current_date)

   # Connect to DynamoDB table
    table = dynamodb.Table('birthday_table')

    #Scan DynamoDB table for students with birthday today
    response = table.scan()
    today_birthday =  [
                       student for student in response['Items']
                       if student['dob'][5:] == current_date
                      ]
   
    #print(today_birthday)
    for std in today_birthday:
        send_birthday_email(std)

    return {
        'statusCode': 200,
        'body': 'Birthday emails sent successfully'
    }

def send_birthday_email(student):
    # Compose email message
    subject = 'Happy Birthday, {}'.format(student['std_name'])
    body_text = 'Dear {},\n\nHappy birthday! We hope you have a fantastic day.\n\nBest regards,\nYour School'.format(student['std_name'])
    sender = 'ritikkaushik74717@gmail.com'
    recipient = student['email']

    # Send email using Amazon SES
    try:
        response = ses.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source=sender
        )
        print("Email sent to", recipient)
    except Exception as e:
        print("Error sending email:", e)
