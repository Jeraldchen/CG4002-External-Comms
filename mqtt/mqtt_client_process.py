from mqtt.mqtt_client import MQTTClient
from multiprocessing import Queue
import json

# send data to visualizer, can have multiple
def mqtt_client_process(topic, to_visualiser_queue: Queue):
    client = MQTTClient(to_visualiser_queue)
    client.connect_mqtt()
    client.send_message(topic)
        
        