from mqtt.mqtt_server import MQTTServer
from multiprocessing import Queue

def mqtt_server_process(topic, from_visualiser_queue: Queue):
    mqtt_server = MQTTServer(from_visualiser_queue)
    mqtt_server.connect_mqtt()
    mqtt_server.receive_message(topic)