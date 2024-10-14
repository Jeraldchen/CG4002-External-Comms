from mqtt.mqtt_client import MQTTClient
from multiprocessing import Queue
import json

# send data to visualizer, can have multiple
def mqtt_client_process(mqtt_publish_queue: Queue):
    client = MQTTClient()
    client.connect_mqtt()
    while True:
        message = mqtt_publish_queue.get()
        message_json = json.loads(message)
        topic = message_json['topic']
        try:
            client.send_message(topic, message)
        except Exception as e:
            print(f"Error sending message to visualizer: {e}")
        