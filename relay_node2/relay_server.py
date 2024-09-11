from socket import *
import threading
import time

class RelayServer:
    def __init__(self, relay_server_port, eval_client_port):
        self.relay_server_port = relay_server_port
        self.eval_client_port = eval_client_port
        self.for_relay_client_socket = socket(AF_INET, SOCK_STREAM)
        self.for_eval_client_socket = socket(AF_INET, SOCK_STREAM)

    def handle_relay_client_and_eval_client(self, relay_client_socket):
        time.sleep(20)
        while True:
            received_message = self.receive_message_relay_client(relay_client_socket)
            # if not received_message:
            #     break
            print(f"Received data from relay client: {received_message}")
            self.send_message_eval_client(received_message)
            print(f"Forwarded data to evaluation client {received_message}")
            # received_message = self.receive_message_eval_client()
            # print(f"Received data from evaluation client: {received_message}")
            # self.send_message_relay_client(received_message)
            # print(f"Forwarded data to relay client {received_message}")
    
    def send_message_eval_client(self, message): # relay server to eval client
        self.for_eval_client_socket.send(f"{len(message)}_".encode()) # must split as message is already encoded but "len(message)_" is not encoded
        self.for_eval_client_socket.send(message.encode())
    
    def receive_message_eval_client(self): # eval client to relay server
        received_message = self.for_eval_client_socket.recv(2048).decode()
        received_message = received_message.split("_", 1)[1] # return the data part of the message
        return received_message
    
    def send_message_relay_client(self, relay_client_socket, message): # relay server to relay client
        relay_client_socket.send(f"{len(message)}_".encode()) # must split as message is already encoded but "len(message)_" is not encoded
        relay_client_socket.send(message.encode()) 
    
    def receive_message_relay_client(self, relay_client_socket): # relay client to relay server
        received_message = relay_client_socket.recv(2048).decode()
        received_message = received_message.split("_", 1)[1] # return the data part of the message
        return received_message # decoded form

    def start_relay_server(self):
        self.for_relay_client_socket.bind(('' , self.relay_server_port))
        self.for_relay_client_socket.listen()
        print("The relay server is ready to receive messages from relay client")
        self.for_eval_client_socket.connect(('127.0.0.1', self.eval_client_port)) # connect to eval client
        while True:
            relay_client_socket, relay_client_addr = self.for_relay_client_socket.accept()
            print("Connection from", relay_client_addr)
            threading.Thread(target=self.handle_relay_client_and_eval_client, args=(relay_client_socket,)).start()