from socket import *
import threading
from evaluation_client2.encryption import AESEncryption
import json
from evaluation_client2.game_state import GameState
import time

class EvalClient:
    def __init__(self, relay_server_port, eval_server_name, eval_server_port, eval_client_port):
        self.eval_client_port = eval_client_port
        self.relay_server_port = relay_server_port
        self.eval_server_name = eval_server_name
        self.eval_server_port = eval_server_port
        self.encryption = AESEncryption()
        self.for_eval_server_socket = socket(AF_INET, SOCK_STREAM)
        self.for_relay_server_socket = socket(AF_INET, SOCK_STREAM)
        self.game_state = GameState()
    
    def handle_relay_server_and_eval_server(self, relay_server_socket):
        time.sleep(20)
        while True:
            received_message =  self.receive_message_relay_server(relay_server_socket)
            # if not received_message:
            #     break
            print(f"Received data from relay server: {received_message}")
            json_data = json.loads(received_message)
            player_id = json_data["player_id"]
            action = json_data["action"]
            if action == "exit":
                break

            data_to_eval_server = {
                "player_id": player_id,
                "action": action,
                "game_state": self.game_state.get_dict()
            }
            
            self.send_message_eval_server(json.dumps(data_to_eval_server))
            print(f"Sent message to evaluation server for player {player_id}: {action}")

            true_game_state = self.receive_message_eval_server()
            print(f"True game state from eval server: {true_game_state}")

    def send_message_eval_server(self, message):
        message = self.encryption.encrypt_and_encode_message(message)
        self.for_eval_server_socket.send(f"{len(message)}_".encode()) # must split as message is already encoded but "len(message)_" is not encoded
        self.for_eval_server_socket.send(message)
    
    def receive_message_eval_server(self):
        received_message = self.for_eval_server_socket.recv(2048).decode()
        received_message = received_message.split("_", 1)[1] # return the data part of the message
        return received_message
    
    def send_message_relay_server(self, relay_server_socket, message):
        relay_server_socket.send(f"{len(message)}_".encode()) # must split as message is already encoded but "len(message)_" is not encoded
        relay_server_socket.send(message.encode())
    
    def receive_message_relay_server(self, relay_server_socket):
        received_message = relay_server_socket.recv(2048).decode()
        received_message = received_message.split("_", 1)[1] # return the data part of the message
        return received_message

    def hello(self):
        self.for_eval_server_socket.connect((self.eval_server_name, self.eval_server_port))
        self.send_message_eval_server("hello")

    def start_eval_client(self):
        self.for_relay_server_socket.bind(('', self.eval_client_port))
        self.for_relay_server_socket.listen()
        print("The evaluation client is ready to receive messages")
        self.hello() # send hello message to the evaluation server and connect to it
        while True:
            relay_server_socket, relay_server_addr = self.for_relay_server_socket.accept()
            print("Connection from", relay_server_addr)
            threading.Thread(target=self.handle_relay_server_and_eval_server, args=(relay_server_socket,)).start()   
        