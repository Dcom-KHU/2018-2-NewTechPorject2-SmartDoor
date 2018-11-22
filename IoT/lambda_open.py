import json
import random
import string
import logging
import boto3
import datetime

client = boto3.client('iot-data')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SmartDoor_Things')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def publish_auth_result(event, context):
    thingName = event['thingName']
    requestId = event['requestId']
    userId = event['userId']
    
    item = table.get_item(Key={'thingName':thingName})
    
    if userId in item['Item']['users']:
        
        JSONPayload = json.dumps(
            {
                "requestId": requestId, 
                "response": "accept", 
                "time": datetime.datetime.now().isoformat()
            })
        
        response = client.publish(
        topic='smartdoor/{}/open/accept'.format(thingName),
        qos=0,
        payload=JSONPayload
        )

    else:
        JSONPayload = json.dumps(
            {
                "requestId": requestId, 
                "response": "rejected", 
                "time": datetime.datetime.now().isoformat()
            })
        
        response = client.publish(
        topic='smartdoor/{}/open/reject'.format(thingName),
        qos=0,
        payload=JSONPayload
        )
        
    logger.info("door open request, detail: {}".format(JSONPayload))
    
    return JSONPayload