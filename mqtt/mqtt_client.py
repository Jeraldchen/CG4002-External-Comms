# This mqtt client is used to obtain the true game state from the game engine and send to the visualiser
# Adapted from https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
from paho.mqtt.client import *

class MQTTClient:
    def __init__(self):
        self.client = self.connect_mqtt()

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected successfully")
            else:
                print(f"Connection failed with code {rc}")
        
        self.client = Client()
        self.client.on_connect = on_connect
        self.client.connect('broker.hivemq.com', 1883, 60)
        return self.client

    def send_message(self, topic, message):
        message = message.encode('utf-8')
        self.client.publish(topic, message) # send the message to the visualiser
        