import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

def testCallback(client, userdata, message):
    print("Recived : ")
    print(message.payload)
    print("topic : ")
    print(message.topic)
    print("----------\n\n")

client = AWSIoTMQTTClient("testClient")

client.configureEndpoint("a3cfl7aqjid92n-ats.iot.ap-northeast-2.amazonaws.com", 8883)
client.configureCredentials("AmazonRootCA1.pem", "18499b1b60-private.pem.key", "18499b1b60-certificate.pem.crt")
client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)  # 10 sec
client.configureMQTTOperationTimeout(5)  # 5 sec

topic = 'test'
client.connect()
client.subscribe(topic, 1, testCallback)
time.sleep(2)

loopCount = 0
while True:
    message = {}
    message['message'] = 'testmessage'
    message['sequence'] = loopCount
    messageJson = json.dumps(message)
    client.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))
    loopCount += 1
    time.sleep(1)
