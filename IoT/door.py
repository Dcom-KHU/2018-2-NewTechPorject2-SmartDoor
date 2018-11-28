from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import actuator

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

    if message.topic.split('/')[-1] == 'accept':
        print('======accept======')
        actuator.setAngle(10)
        actuator.setAngle(0)
    elif message.topic.split('/')[-1] == 'reject':
        print('======reject======')


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
    client.subscribe(topic+'/accept', 1, customCallback)
    client.subscribe(topic+'/reject', 1, customCallback)
    time.sleep(2)


def publishOpen(client, topic, message):
    # Publish to the same topic 
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
            message = {'userId': 'User2'}
            publishOpen(client, topic, message)
        if (i+11) % 20 == 0:
            message = {'userId': 'User1'}
            publishOpen(client, topic, message)
        time.sleep(1)


if __name__ == "__main__":
    istest = True
    
    if istest == True:
        test()
    else:
        main()
