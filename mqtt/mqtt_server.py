#from multiprocessing import Queue
from paho.mqtt.client import *

class MQTTServer:
    def __init__(self):
        self.message_payload = None

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
        print(self.message_payload)

    def receive_message(self): # receive message from the visualizer
        self.client.on_message = self.on_message
        self.client.subscribe("detection")
        self.client.loop_forever()