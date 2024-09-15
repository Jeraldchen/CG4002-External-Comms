from mqtt.mqtt_client import MQTTClient
from multiprocessing import Queue
import json


def mqtt_client_process(from_ai_to_eval_client_queue: Queue):
    client = MQTTClient()
    while True:
        message = from_ai_to_eval_client_queue.get()
        message_json = json.loads(message)
        player_id = message_json["player_id"]
        action = message_json["action"]
        topic_p1 = "player1/action"
        topic_p2 = "player2/action"
        if player_id == 1:
            topic = topic_p1
        else:
            topic = topic_p2
        client.send_message(topic, action) # send action to visualizer
        