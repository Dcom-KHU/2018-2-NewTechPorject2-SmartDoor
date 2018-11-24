from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import json
from pprint import pprint 

class CallbackHandler:
    def __init__(self, deviceShadowInstance):
        self.deviceShadowInstance = deviceShadowInstance 

    def updateCallback(self, payload, responseStatus, token):
        if responseStatus == "timeout":
            print("Update request " + token + " time out!")
        if responseStatus == "accepted":
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
        payload = json.loads(payload)
        new_state = payload['state']['state']
        new_id = payload['state']['doorid']
        # state update
        JSONPayload = json.dumps({"state":{"desired":None, "reported":{"state":new_state, "doorid":new_id}}})
        self.deviceShadowInstance.shadowUpdate(JSONPayload, self.updateCallback, 5)