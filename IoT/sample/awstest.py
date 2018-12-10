import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


# read config
def readConfig(configFile):
    with open(configFile) as f:
        conf = json.load(f)
    return conf

# make client
def makeClient(clientInfo):
    client = AWSIoTMQTTClient(clientInfo['clientID']) # make client with client ID
    client.configureEndpoint(clientInfo['endpoint'], int(clientInfo['port'])) # set endpoint and port
    client.configureCredentials(clientInfo['rootCA'], clientInfo['key'], clientInfo['cert']) # set credentials
    
    client.configureAutoReconnectBackoffTime(1, 32, 20) #
    client.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing 
    client.configureDrainingFrequency(2)  # Draining: 2 Hz
    client.configureConnectDisconnectTimeout(10)  # 10 sec
    client.configureMQTTOperationTimeout(5)  # 5 sec

    return client

# basic callback
def testCallback(client, userdata, message):
    print("Recived : ")
    print(message.payload)
    print("topic : ")
    print(message.topic)
    print("----------\n\n")


configFile = 'config.json'
config = readConfig(configFile)

shadowUpdateTopic = '$aws/things/{}/shadow/update/'.format(config['thingName'])
shadowDeleteTopic = '$aws/things/{}/shadow/delete/'.format(config['thingName'])

client = makeClient(config)
client.connect()
client.subscribe(shadowUpdateTopic, 1, testCallback)
client.subscribe(shadowUpdateTopic+'#', 1, testCallback)
client.subscribe(shadowDeleteTopic+'#', 1, testCallback)
time.sleep(2)

client.publish(shadowDeleteTopic, '{"version": 822, "timestamp": 1540442793}', 1)
print('Published topic %s\n' % (shadowDeleteTopic))
time.sleep(2)

message = {'state': {'reported': {'doorid': 'testmessage'}}}
messageJson = json.dumps(message)
client.publish(shadowUpdateTopic, messageJson, 1)
print('Published topic %s: %s\n' % (shadowUpdateTopic, messageJson))

while True:
    time.sleep(1)
