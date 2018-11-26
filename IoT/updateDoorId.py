from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import datetime
import json
from pprint import pprint 

class CallbackHandler:
    def __init__(self, deviceShadowInstance):
        self.deviceShadowInstance = deviceShadowInstance 

    def updateCallback(self, payload, responseStatus, token):
        if responseStatus == "timeout":
            print("Update request " + token + " time out!")
        if responseStatus == "accepted":
            payloadDict = json.loads(payload)
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            print("Update request with token: " + token + " accepted!")
            pprint(json.loads(payload))
            print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        if responseStatus == "rejected":
            print("Update request " + token + " rejected!")

    def deleteCallback(self, payload, responseStatus, token):
        if responseStatus == "timeout":
            print("Delete request " + token + " time out!")
        if responseStatus == "accepted":
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            print("Delete request with token: " + token + " accepted!")
            print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        if responseStatus == "rejected":
            print("Delete request " + token + " rejected!")

    def deltaCallback(self, payload, responseStatus, token):
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Delta request ")
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")

        # update state
        pprint(payload)
        payload = json.loads(payload)
        new_state = payload['state']['state']
        new_id = payload['state']['doorid']
        # state update
        JSONPayload = json.dumps({"state":{"reported":{"state":new_state, "doorid":new_id}}})
        self.deviceShadowInstance.shadowUpdate(JSONPayload, self.updateCallback, 5)

def buildMQTTShadowClient(configFile):
    # read config
    with open(configFile) as f:
        conf = json.load(f)

    # init shadow client
    client = AWSIoTMQTTShadowClient(conf['clientID'])
    client.configureEndpoint(conf['endpoint'], int(conf['port']))
    client.configureCredentials(conf['rootCA'], conf['key'], conf['cert'])

    # client config
    client.configureAutoReconnectBackoffTime(1, 32, 20)
    client.configureConnectDisconnectTimeout(10)  # 10 sec
    client.configureMQTTOperationTimeout(5)  # 5 sec

    return client, conf


def request_id(deviceShadowHandler, handler):

        # init state
        # Request new door id
        JSONPayload = json.dumps({"state":{"desired":{"state":"RequestNewID"}, "reported":{"state":"RequestNewID"}}})
        deviceShadowHandler.shadowUpdate(JSONPayload, handler.updateCallback, 5)


def main():
    client, conf = buildMQTTShadowClient('config.json') 

    # connect
    client.connect()

    # create a deviceShadow
    deviceShadowHandler = client.createShadowHandlerWithName(conf['thingName'], True)
    handler = CallbackHandler(deviceShadowHandler)

    # delete shadow json 
    deviceShadowHandler.shadowDelete(handler.deleteCallback, 5)

    # Register shadow delta callback
    deviceShadowHandler.shadowRegisterDeltaCallback(handler.deltaCallback)
    
    request_id(deviceShadowHandler, handler)

    i = 0
    # loop
    while True:
       i+=1
       time.sleep(1)
       if i % 10 == 0:
           request_id(deviceShadowHandler, handler)


if __name__ == '__main__':
    main()
