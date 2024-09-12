from multiprocessing import Queue
from evaluation_client.evaluation_client import EvaluationClient

def evaluation_client_process(send_eval_server_game_state_queue: Queue, receive_eval_server_game_state_queue: Queue, server_name, server_port):
    client = EvaluationClient(server_name, server_port)
    client.hello() # connect to server
    
    while True:
        ai_predicted_game_state = send_eval_server_game_state_queue.get() # get game state from AI
        client.send_message(ai_predicted_game_state) # send game state to eval server
        true_game_state = client.receive_message() # receive true game state from eval server
        receive_eval_server_game_state_queue.put(true_game_state) # send true game state to queue
    