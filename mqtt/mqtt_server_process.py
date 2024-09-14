from mqtt.mqtt_server import MQTTServer

def mqtt_server_process():
    mqtt_server = MQTTServer()
    mqtt_server.connect_mqtt()
    mqtt_server.receive_message()