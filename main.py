from multiprocessing import *
from relay_node.relay_node_server_process import relay_node_server_process
from evaluation_client.evaluation_client_process import evaluation_client_process
# # from game_engine.game_engine_process import game_engine_process
# # from ai.ai_process import ai_process
# from mqtt.mqtt_client_process import mqtt_client_process
# from mqtt.mqtt_server_process import mqtt_server_process

if __name__ == '__main__':

    eval_server_port = int(input("Enter the port number for the evaluation server: "))

    # Create queues
    relay_to_ai_queue = Queue() # relay to ai
    eval_to_relay_queue_player1 = Queue() # eval to relay
    eval_to_relay_queue_player2 = Queue() # eval to relay
    ai_to_visualiser_queue = Queue() # ai to visualiser
    eval_to_visualiser_queue = Queue() # eval to visualiser
    visualiser_to_eval_queue = Queue() # visualiser to eval
    
    

    # Create processes
    relay_node_server_player1 = Process(target=relay_node_server_process, args=(relay_to_ai_queue, eval_to_relay_queue_player1, 8800)) # send IMU to AI and send true game state to internal comms
    relay_node_server_player2 = Process(target=relay_node_server_process, args=(relay_to_ai_queue, eval_to_relay_queue_player2, 8801)) # send IMU to AI and send true game state to internal comms
    # mqtt_client_ai_to_visualiser = Process(target=mqtt_client_process, args=("ai/action", ai_to_visualiser_queue)) # send action to visualiser
    # mqtt_client_eval_to_visualiser = Process(target=mqtt_client_process, args=("eval/game_state", eval_to_visualiser_queue)) # send true game state to visualiser
    # mqtt_server_visualiser_to_eval = Process(target=mqtt_server_process, args=("ai/game_state", visualiser_to_eval_queue)) # get ai predicted game state and send to eval server
    # eval_client = Process(target=evaluation_client_process, args=(visualiser_to_eval_queue, eval_to_visualiser_queue, eval_to_relay_queue_player1, eval_to_relay_queue_player2, 'localhost', eval_server_port)) # send true game state to eval server
    eval_client = Process(target=evaluation_client_process, args=(relay_to_ai_queue, eval_to_visualiser_queue, eval_to_relay_queue_player1, eval_to_relay_queue_player2, 'localhost', eval_server_port)) # send true game state to eval server

    # ai = Process(target=ai, args=(relay_to_ai_queue, ai_to_visualiser_queue)) # For Phone

    

    # Start processes
    relay_node_server_player1.start()
    relay_node_server_player2.start()
    # mqtt_client_ai_to_visualiser.start()
    # mqtt_client_eval_to_visualiser.start()
    # mqtt_server_visualiser_to_eval.start()
    eval_client.start()
    # ai.start()

    # Join processes
    relay_node_server_player1.join()
    relay_node_server_player2.join()
    # mqtt_client_ai_to_visualiser.join()
    # mqtt_client_eval_to_visualiser.join()
    # mqtt_server_visualiser_to_eval.join()
    eval_client.join()
    # ai.join()