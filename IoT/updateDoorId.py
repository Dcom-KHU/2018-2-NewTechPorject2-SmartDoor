from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import datetime
import json
from pprint import pprint 
from ShadowCallbackHandler import CallbackHandler

def buildMQTTShadowClient(configFile):
    # read config
    with open(configFile) as f:
        conf = json.load(f)

    # init shadow client
    client = AWSIoTMQTTShadowClient(conf['thingName']+'_shadow')
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

# update Door id with shadow
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
