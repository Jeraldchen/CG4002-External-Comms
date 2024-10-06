from game_engine.game_state import GameState
from mqtt.mqtt_server import MQTTServer
import json
from multiprocessing import Queue

def ai_process(p1_action: Queue, p2_action: Queue):
    mqtt_server = MQTTServer()
    mqtt_server.connect_mqtt()
    mqtt_server.receive_message("action/AI") # receive interpreted action from AI

    while True:
        ai_action_data = mqtt_server.message_payload
        ai_action_data_json = json.loads(ai_action_data)
        player_id = ai_action_data_json["player_id"]
        if player_id == 1:
            p1_action.put(ai_action_data_json)
        else:
            p2_action.put(ai_action_data_json)


        