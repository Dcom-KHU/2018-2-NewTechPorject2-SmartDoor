import json
import random
import string
import logging
import boto3

client = boto3.client('iot-data')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def UpdateShadow(event, context):
    id = genereateRandomString()
    thingName = event['thingName']
    logger.info('Request From "{}", state: {}'\
        .format(thingName, event['state']['desired']))
    
    JSONPayload = json.dumps({"state":{"desired":{"state":"Active", "doorid":id}}})
    client.update_thing_shadow(thingName=thingName, payload=JSONPayload)
    
    return id

def genereateRandomString(k=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

