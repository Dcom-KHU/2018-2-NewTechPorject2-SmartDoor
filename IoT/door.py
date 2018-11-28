from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


def openAcceptCallback(client, userdata, message):
    print("Received a open accept")
    
    customCallback(client, userdata, message)

    # do open door


def buildMQTTClient(configFile):
    # read config
    with open(configFile) as f:
        conf = json.load(f)

    # init client
    client = AWSIoTMQTTClient(conf['thingName']+'_basic')
    client.configureEndpoint(conf['endpoint'], int(conf['port']))
    client.configureCredentials(conf['rootCA'], conf['key'], conf['cert'])

    # client config
    client.configureAutoReconnectBackoffTime(1, 32, 20)
    client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    client.configureAutoReconnectBackoffTime(1, 32, 20)
    client.configureConnectDisconnectTimeout(10)  # 10 sec
    client.configureMQTTOperationTimeout(5)  # 5 sec

    return client, conf


def setLogger():
    # Configure logging
    logger = logging.getLogger("AWSIoTPythonSDK.core")
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)


def subscribeOpen(client, topic):

    # subscribe topic
    client.subscribe(topic, 1, customCallback)
    client.subscribe(topic+'/accept', 1, openAcceptCallback)
    client.subscribe(topic+'/reject', 1, customCallback)
    time.sleep(2)


def publishOpen(client, topic):
    # Publish to the same topic 
    message = {}
    message['thingName'] = 'open'
    message['requestId'] = 'testid'
    message['userId'] = 'User1'
    messageJson = json.dumps(message)
    client.publish(topic, messageJson, 1)

    print('Published topic %s: %s\n' % (topic, messageJson))


def main():
    setLogger()

    # Connect and subscribe to AWS IoT
    client, conf = buildMQTTClient('config.json')
    client.connect()

    # open topic
    topic = 'smartdoor/'+ conf['thingName'] +'/open'

    subscribeOpen(client, topic)

    return client, topic

def test():
    client, topic = main()

    i = 0
    while True:
        i+=1
        if i % 10 == 0:
            publishOpen(client, topic)
        time.sleep(1)


if __name__ == "__main__":
    istest = True
    
    if istest == True:
        test()
    else:
        main()
