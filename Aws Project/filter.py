import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('StudentTable')
    l1=["class","marks"]
    x=None
    l2=list(event.keys())
    print(l2)
    for i in l1:
        if i==l2[0]:
            x=i
        
    print(x)   
    if x==l1[0]:  
         marks_threshold = str(event[x])
    else:
        marks_threshold = int(event[x])
    print(marks_threshold)
    op=event['operator']
    print(op)

    # Define the filter expression for marks greater than 60
    filter_expression = "#attribute ? :attribute_value"
    filter_expression =filter_expression.replace("?",op)
    expression_attribute_names = {"#attribute": x}
    expression_attribute_values = {":attribute_value": marks_threshold}

    # Perform the query
    response = table.scan(FilterExpression=filter_expression,
                          ExpressionAttributeNames=expression_attribute_names,
                          ExpressionAttributeValues=expression_attribute_values)

    # Extract the filtered items
    filtered_items = response['Items']
    print(filtered_items,type(filtered_items))

    return filtered_items
