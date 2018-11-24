from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

AllowedActions = ['both', 'publish', 'subscribe']

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

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


def main():
    client, conf = buildMQTTClient('config.json')

    # open topic
    topic = 'smartdoor/'+ conf['thingName'] +'/open'

    # Configure logging
    logger = logging.getLogger("AWSIoTPythonSDK.core")
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    # Connect and subscribe to AWS IoT
    client.connect()

    # subscribe topic
    client.subscribe(topic, 1, customCallback)
    time.sleep(2)

    # Publish to the same topic 
    message = {}
    message['message'] = 'open'
    messageJson = json.dumps(message)
    client.publish(topic, messageJson, 1)
    # if args.mode == 'publish':
    print('Published topic %s: %s\n' % (topic, messageJson))
    time.sleep(5)


if __name__ == "__main__":
    main()
