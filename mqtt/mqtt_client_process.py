from mqtt.mqtt_client import MQTTClient
from multiprocessing import Queue
import json


def mqtt_client_process(from_ai_to_eval_client_queue: Queue):
    client = MQTTClient()
    while True:
        message = from_ai_to_eval_client_queue.get()
        message_json = json.loads(message)
        action = message_json["action"]
        topic = "action"
        client.send_message(topic, action) # send action to visualizer
        