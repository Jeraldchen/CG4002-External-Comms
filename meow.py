import sys
from paho.mqtt.client import Client
import json

class MQTTClient:
    def __init__(self):
        self.client = self.connect_mqtt()

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected successfully")
            else:
                print(f"Connection failed with code {rc}")
        
        client = Client()
        client.on_connect = on_connect
        client.connect('68.183.180.79', 1883, 300)
        return client

    def send_message(self, topic, message):
        print("Sending to MQTT:", message)
        message = message.encode('utf-8')
        self.client.publish(topic, message) # send the message to the visualiser

mqtt_request_detection = {
    "topic": "visualiser/request_detection",
    "request": "true",
    "player_id": 2
}

def main():
    mqtt_client = MQTTClient()
    
    # Prompt the user for the topic and message
    topic = mqtt_request_detection['topic']
    message = json.loads(mqtt_request_detection)
    
    # Send the message
    mqtt_client.send_message(topic, message)
    
    # Keep the script running to maintain the connection
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()