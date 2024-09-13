from multiprocessing import *
from relay_node.relay_node_server_process import relay_node_server_process
from evaluation_client.evaluation_client_process import evaluation_client_process
from game_engine.game_engine_process import game_engine_process
from ai.ai_process import ai_process

if __name__ == '__main__':

    eval_server_port = int(input("Enter the port number for the evaluation server: "))

    # Create queues
    relay_to_ai_queue = Queue()
    ai_to_eval_queue = Queue()
    eval_to_game_engine_queue = Queue()
    game_engine_to_relay_queue = Queue()

    # Create processes
    relay_node_server = Process(target=relay_node_server_process, args=(relay_to_ai_queue, game_engine_to_relay_queue, 8800))
    eval_client = Process(target=evaluation_client_process, args=(ai_to_eval_queue, eval_to_game_engine_queue, 'localhost', eval_server_port))
    game_engine = Process(target=game_engine_process, args=(eval_to_game_engine_queue, game_engine_to_relay_queue))
    ai = Process(target=ai_process, args=(relay_to_ai_queue, ai_to_eval_queue))

    # Start processes
    relay_node_server.start()
    eval_client.start()
    game_engine.start()
    ai.start()

    # Join processes
    relay_node_server.join()
    eval_client.join()
    game_engine.join()
    ai.join()