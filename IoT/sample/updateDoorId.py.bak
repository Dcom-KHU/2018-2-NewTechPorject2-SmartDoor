from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import datetime
import json

def updateCallback(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update request with token: " + token + " accepted!")
        print("doorid: " + str(payloadDict["state"]["reported"]["doorid"]))
        print("location: " + str(payloadDict["state"]["reported"]["location"]))
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")

def deleteCallback(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Delete request " + token + " time out!")
    if responseStatus == "accepted":
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Delete request with token: " + token + " accepted!")
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Delete request " + token + " rejected!")

# read config
with open('config.json') as f:
    conf = json.load(f)
    
    endpoint = conf['endpoint']
    rootCA = conf['rootCA']
    cert = conf['cert']
    key = conf['key']
    port = int(conf['port'])
    clientId = conf['clientId']
    thingName = conf['thingName']

# logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# init shadow client
client = AWSIoTMQTTShadowClient(clientId)
client.configureEndpoint(endpoint, port)
client.configureCredentials(rootCA, key, cert)

# client config
client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureConnectDisconnectTimeout(10)  # 10 sec
client.configureMQTTOperationTimeout(5)  # 5 sec

# connect
client.connect()

# create a deviceShadow with persistent subscription
deviceShadowHandler = client.createShadowHandlerWithName(thingName, True)

# delete shadow json doc
deviceShadowHandler.shadowDelete(deleteCallback, 5)

# update shadow
while True:
    with open('state.json') as jsonfile:
        JSONPayload = json.dumps(json.load(jsonfile))
    deviceShadowHandler.shadowUpdate(JSONPayload, updateCallback, 5)
    time.sleep(10)
