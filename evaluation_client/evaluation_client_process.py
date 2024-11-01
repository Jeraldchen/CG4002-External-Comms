from multiprocessing import Queue
from evaluation_client.evaluation_client import EvaluationClient

def evaluation_client_process(from_game_engine: Queue, to_game_engine: Queue, server_name, server_port):
    client = EvaluationClient(server_name, server_port)
    client.hello() # connect to server
    
    while True:
        ai_predicted_game_state = from_game_engine.get() # format must be data = {"player_id": 1, "action": basket, game_state: game_state}, game_state = {p1: xxxxx, p2: xxxxx)}
        print("sent", ai_predicted_game_state)
        client.send_message(ai_predicted_game_state) # send game state to eval server
        true_game_state = client.receive_message()
        print("true", true_game_state)
        to_game_engine.put(true_game_state) # send true game state to visualiser and update game engine
    