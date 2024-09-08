from socket import *

class RelayNodeClient:
    def __init__(self, server_name, server_port):
        self.server_name = server_name
        self.server_port = server_port
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.server_name, self.server_port))

    def send_message(self, message):
        self.socket.send(f"{len(message)}_{message}".encode())
        
    def receive_message(self):
        received_message = self.socket.recv(2048).decode()
        received_message = received_message.split("_", 1)[1] # return the data part of the message
        return received_message
        