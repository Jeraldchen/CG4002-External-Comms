# This mqtt client is used to obtain the true game state from the game engine and send to the visualiser
# Adapted from https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
from paho.mqtt.client import *
from multiprocessing import Queue

class MQTTClient:
    def __init__(self, to_visualiser_queue: Queue):
        self.client = self.connect_mqtt()
        self.to_visualiser_queue = to_visualiser_queue # queue to send game state data to visualiser from eval server

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

    def send_message(self, topic):
        message = self.to_visualiser_queue.get() # data to be sent tpo the visualiser (game state, action etc)
        self.client.publish(topic, message) # send the message to the visualiser
        