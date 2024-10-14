from multiprocessing import *
from relay_node.relay_node_server_process import relay_node_server_process
from evaluation_client.evaluation_client_process import evaluation_client_process
from game_engine.game_engine_process import game_engine_process
# from ai.ai_process import ai_process
from mqtt.mqtt_client_process import mqtt_client_process
from mqtt.mqtt_server_process import mqtt_server_process

if __name__ == '__main__':

    eval_server_port = int(input("Enter the port number for the evaluation server: "))

    # Create queues
    mqtt_publish_queue = Queue() 
    mqtt_subscribe_queue = Queue() 
    ai_action_queue = Queue() 
    ai_game_state_send_to_eval_server_queue = Queue() 
    send_to_relay_node_queue = Queue() 
    true_game_state_from_eval_server_queue = Queue()
    shoot_action_queue = Queue()
    got_shot_queue = Queue()
    
    

    # Create processes
    relay_node_server = Process(target=relay_node_server_process, args=(ai_action_queue, send_to_relay_node_queue, shoot_action_queue, got_shot_queue, 8800)) # send IMU to AI and send true game state to internal comms
    mqtt_client = Process(target=mqtt_client_process, args=(mqtt_publish_queue,)) 
    mqtt_server = Process(target=mqtt_server_process, args=(mqtt_subscribe_queue,)) # get ai predicted game state and send to eval server
    eval_client = Process(target=evaluation_client_process, args=(ai_game_state_send_to_eval_server_queue, true_game_state_from_eval_server_queue, 'localhost', eval_server_port)) # send true game state to eval server
    # ai = Process(target=ai, args=(relay_to_ai_queue, ai_to_visualiser_queue)) # For Phone
    game_engine = Process(target=game_engine_process, args=(mqtt_publish_queue, mqtt_subscribe_queue, ai_action_queue, ai_game_state_send_to_eval_server_queue, send_to_relay_node_queue, true_game_state_from_eval_server_queue, shoot_action_queue, got_shot_queue)) 

    

    # Start processes
    relay_node_server.start()
    mqtt_client.start()
    mqtt_server.start()
    eval_client.start()
    # ai.start()
    game_engine.start()

    # Join processes
    relay_node_server.join()
    mqtt_client.join()
    mqtt_server.join()
    eval_client.join()
    # ai.join()
    game_engine.join()