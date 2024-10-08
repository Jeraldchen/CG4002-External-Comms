from multiprocessing import Queue
from evaluation_client.evaluation_client import EvaluationClient

def evaluation_client_process(from_visualiser: Queue, to_visualiser: Queue, to_relay_node: Queue, server_name, server_port):
    client = EvaluationClient(server_name, server_port)
    client.hello() # connect to server
    
    while True:
        ai_predicted_game_state = from_visualiser.get() # format must be data = {"player_id": 1, "action": basket, game_state: game_state}, game_state = {p1: xxxxx, p2: xxxxx)}
        client.send_message(ai_predicted_game_state) # send game state to eval server
        true_game_state = client.receive_message()
        to_visualiser.put(true_game_state) # send true game state to visualiser and update game engine
        to_relay_node.put(true_game_state) # send true game state to relay node to update hardware via internal comms
    