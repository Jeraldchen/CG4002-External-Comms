from multiprocessing import Queue
from relay_node.relay_node_server import RelayNodeServer

def relay_node_server_process(server_port, send_eval_server_game_state_queue: Queue, receive_eval_server_game_state_queue: Queue):
    server = RelayNodeServer(server_port)
    server.run(send_eval_server_game_state_queue, receive_eval_server_game_state_queue)
