from paho.mqtt.client import *
from multiprocessing import Queue

class MQTTServer:
    def __init__(self, mqtt_subscribe_queue: Queue):
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
        if message.topic == "visualiser/detection_state":
            self.mqtt_subscribe_queue.put(message.payload.decode())


    def receive_message(self): # receive message from the visualizer
        self.client.on_message = self.on_message
        self.client.subscribe("visualiser/detection_state")
        self.client.loop_forever()