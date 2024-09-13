from game_engine.game_state import GameState
import json
from multiprocessing import Queue

def ai_process(from_relay_server_queue: Queue, to_eval_server_queue: Queue):
    game_state = GameState()
    while True:
        data = from_relay_server_queue.get() # get the message from the relay node
        data = json.loads(data)
        player_id = data["player_id"]
        action = data["action"]

        data_to_send = {
            "player_id": player_id,
            "action": action,
            "game_state": game_state.get_dict()
        }

        to_eval_server_queue.put(json.dumps(data_to_send)) # send to eval client
        


        