from paho.mqtt.client import *
from multiprocessing import Queue

class MQTTServer:
    def __init__(self, mqtt_subscribe_queue: Queue):
        self.message_payload = None
        self.mqtt_subscribe_queue = mqtt_subscribe_queue


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
    
    def on_message(self, client, userdata, message):
        self.message_payload = message.payload.decode()
        self.mqtt_subscribe_queue.put(self.message_payload) # put detection state and num of rain bombs data from visualizer to the queue
        # print(self.message_payload)

    def run(self, topic): # receive message from the visualizer
        self.client.on_message = self.on_message
        self.client.subscribe(topic)
        self.client.loop_forever()