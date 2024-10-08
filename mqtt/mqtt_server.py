from paho.mqtt.client import *
from multiprocessing import Queue

class MQTTServer:
    def __init__(self, from_visualiser_queue: Queue):
        self.message_payload = None
        self.from_visualiser_queue = from_visualiser_queue

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
        self.from_visualiser_queue.put(self.message_payload) # put data from visualiser into the queue, data will be in json format, consists of player id, player game state and detection state
        print(self.message_payload)

    def receive_message(self, topic): # receive message from the visualizer
        self.client.on_message = self.on_message
        self.client.subscribe(topic)
        self.client.loop_forever()