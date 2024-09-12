from multiprocessing import Queue
from game_engine.game_state import GameState
import json

def game_engine_process(from_eval_client_queue: Queue, to_relay_server_queue: Queue):
    game_state = GameState()
    while True:
        game_state.update_game_state(from_eval_client_queue) # get true game state from eval client
        to_relay_server_queue.put(json.dumps(game_state.get_dict())) # send to relay node