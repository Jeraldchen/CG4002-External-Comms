from multiprocessing import Queue
from relay_node.relay_node_server import RelayNodeServer

def relay_node_server_process(to_ai_queue: Queue, receive_eval_server_game_state_queue: Queue, server_port):
    try:
        server = RelayNodeServer(server_port)
        server.run(to_ai_queue, receive_eval_server_game_state_queue)
    except Exception as e:
        print("Error in relay node server process:", e)
