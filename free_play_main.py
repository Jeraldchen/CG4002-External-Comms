from multiprocessing import *
from relay_node.relay_node_server_process import relay_node_server_process
# from evaluation_client.evaluation_client_process import evaluation_client_process
from game_engine.free_play_game_engine_process import free_play_game_engine_process
from ai.ai_process import ai_process
from mqtt.mqtt_client_process import mqtt_client_process
from mqtt.mqtt_server_process import mqtt_server_process

if __name__ == '__main__':
    try:
        # eval_server_port = int(input("Enter the port number for the evaluation server: "))

        # Create queues
        mqtt_publish_queue = Queue() 
        mqtt_subscribe_queue = Queue()  
        ai_game_state_send_to_eval_server_queue = Queue() 
        
        send_to_relay_node_queue_player1 = Queue()
        send_to_relay_node_queue_player1_dupe = Queue()
        send_to_relay_node_queue_player2 = Queue()
        send_to_relay_node_queue_player2_dupe = Queue() 
        
        true_game_state_from_eval_server_queue = Queue()
        shoot_action_queue = Queue()
        got_shot_queue = Queue()
        to_ai_queue = Queue()
        from_ai_queue = Queue()
        
        

        # Create processes
        relay_node_server_player1 = Process(target=relay_node_server_process, args=(to_ai_queue, send_to_relay_node_queue_player1, shoot_action_queue, got_shot_queue, 8800, from_ai_queue)) # send IMU to AI and send true game state to internal comms
        relay_node_server_player2 = Process(target=relay_node_server_process, args=(to_ai_queue, send_to_relay_node_queue_player2, shoot_action_queue, got_shot_queue, 8801, from_ai_queue)) # send IMU to AI and send true game state to internal comms
        relay_node_server_player1_dupe = Process(target=relay_node_server_process, args=(to_ai_queue, send_to_relay_node_queue_player1_dupe, shoot_action_queue, got_shot_queue, 8802, from_ai_queue)) # send IMU to AI and send true game state to internal comms
        relay_node_server_player2_dupe = Process(target=relay_node_server_process, args=(to_ai_queue, send_to_relay_node_queue_player2_dupe, shoot_action_queue, got_shot_queue, 8803, from_ai_queue)) # send IMU to AI and send true game state to internal comms
        # relay_node_server_AI = Process(target=relay_node_server_process, args=(to_ai_queue, send_to_relay_node_queue_player2, shoot_action_queue, got_shot_queue, 8802, from_ai_queue)) # send IMU to AI and send true game state to internal comms
        mqtt_client = Process(target=mqtt_client_process, args=(mqtt_publish_queue,)) 
        mqtt_server = Process(target=mqtt_server_process, args=(mqtt_subscribe_queue,)) # get ai predicted game state and send to eval server
        # eval_client = Process(target=evaluation_client_process, args=(ai_game_state_send_to_eval_server_queue, true_game_state_from_eval_server_queue, 'localhost', eval_server_port)) # send true game state to eval server
        ai = Process(target=ai_process, args=(to_ai_queue, from_ai_queue)) # For Phone
        free_play_game_engine = Process(target=free_play_game_engine_process, args=(mqtt_publish_queue, mqtt_subscribe_queue, from_ai_queue, send_to_relay_node_queue_player1, send_to_relay_node_queue_player2, send_to_relay_node_queue_player1_dupe, send_to_relay_node_queue_player2_dupe, shoot_action_queue, got_shot_queue)) 
        

        # Start processes
        relay_node_server_player1.start()
        relay_node_server_player2.start()
        relay_node_server_player1_dupe.start()
        relay_node_server_player2_dupe.start()
        # relay_node_server_AI.start()
        mqtt_client.start()
        mqtt_server.start()
        # eval_client.start()
        ai.start()
        free_play_game_engine.start()

        # Join processes
        relay_node_server_player1.join()
        relay_node_server_player2.join()
        relay_node_server_player1_dupe.join()
        relay_node_server_player2_dupe.join()
        # relay_node_server_AI.join()
        mqtt_client.join()
        mqtt_server.join()
        # eval_client.join()
        ai.join()
        free_play_game_engine.join() 
    except (KeyboardInterrupt, SystemExit):
        relay_node_server_player1.terminate()
        relay_node_server_player2.terminate()
        relay_node_server_player1_dupe.terminate()
        relay_node_server_player2_dupe.terminate()
        # relay_node_server_AI.terminate()
        mqtt_client.terminate()
        mqtt_server.terminate()
        # eval_client.terminate()
        ai.terminate()
        free_play_game_engine.terminate()