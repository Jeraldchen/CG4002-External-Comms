from mqtt.mqtt_server import MQTTServer
from multiprocessing import Queue

def mqtt_server_process(mqtt_subscribe_queue: Queue):
    try:
        mqtt_server = MQTTServer(mqtt_subscribe_queue)
        mqtt_server.connect_mqtt()
        mqtt_server.receive_message()
    except Exception as e:
        print(f"Error in mqtt server process: {e}")