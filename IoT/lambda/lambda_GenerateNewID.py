import json
import random
import string
import logging
import boto3

client = boto3.client('iot-data')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SmartDoor_Things')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def UpdateShadow(event, context):
    id = genereateRandomString()
    thingName = event['thingName']
    logger.info('Request From "{}", state: {}'
        .format(thingName, event['state']['desired']))
    
    JSONPayload = json.dumps({"state":{"desired":{"state":"Active", "doorid":id}}})
    client.update_thing_shadow(thingName=thingName, payload=JSONPayload)
    
    logger.info('Response to "{}", state: {}'
        .format(thingName, JSONPayload))
    
    Update_ThingInfo(thingName, id)
    logger.info('Update Thing info of "{}", state: {}'
        .format(thingName, JSONPayload))
    
    return id

def genereateRandomString(k=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def Update_ThingInfo(thingName, id):
    
    item = table.get_item(Key={'thingName':thingName})
    
    if item != None:
        response = table.update_item(Key={'thingName':thingName}, 
            UpdateExpression="SET doorID = :id",  
            ExpressionAttributeValues={
                ':id': id,
            },
            ReturnValues="UPDATED_NEW")
    else:
        response = dynamodb.put_item(Item={'thingName': thingName, 'doorID':id})
        
    return response
