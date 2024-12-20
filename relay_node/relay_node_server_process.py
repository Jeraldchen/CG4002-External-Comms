from multiprocessing import Queue
from relay_node.relay_node_server import RelayNodeServer

def relay_node_server_process(to_ai_queue: Queue, receive_eval_server_game_state_queue: Queue, shoot_action_queue: Queue, got_shot_queue: Queue, server_port, from_ai_queue: Queue):
    try:
        server = RelayNodeServer(server_port)
        server.run(to_ai_queue, receive_eval_server_game_state_queue, shoot_action_queue, got_shot_queue, from_ai_queue)
    except Exception as e:
        print("Error in relay node server process:", e)
