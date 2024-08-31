import json
import boto3


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EventRegistrations')

def lambda_handler(event, context):
 
    action = event.get('action', 'get_registrations')
    
    if action == 'register':
        # Register a new user
        registration_id = event['registration_id']
        event_id = event['event_id']
        name = event['name']
        email = event['email']
        registration_date = event['registration_date']
        
        # Put item into DynamoDB
        response = table.put_item(Item={
            'RegistrationID': registration_id,
            'EventID': event_id,
            'Name': name,
            'Email': email,
            'RegistrationDate': registration_date
        })
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Registration successful!', 'registration_id': registration_id})
        }
    
    elif action == 'get_registrations':
        # Retrieve registrations for a specific event
        event_id = event['event_id']
        
        # Query DynamoDB for registrations with the specified EventID
        response = table.query(
            IndexName='EventID-index',  # Ensure you have created a Global Secondary Index on EventID
            KeyConditionExpression=boto3.dynamodb.conditions.Key('EventID').eq(event_id)
        )
        
        registrations = response.get('Items', [])
        
        return {
            'statusCode': 200,
            'body': json.dumps({'registrations': registrations})
        }
    
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid action specified'})
        }
