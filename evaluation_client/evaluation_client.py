from socket import *
from encryption import AESEncryption

class EvaluationClient:
    def __init__(self, server_name, server_port):
        self.server_name = server_name
        self.server_port = server_port
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.encryption = AESEncryption()

    def send_message(self, message):
        message = self.encryption.encrypt_and_encode_message(message)
        self.socket.send(f"{len(message)}_".encode()) # must split as message is already encoded but "len(message)_" is not encoded
        self.socket.send(message)

    def hello(self):
        self.socket.connect((self.server_name, self.server_port))
        self.send_message("hello")
        
    def receive_message(self):
        received_message = self.socket.recv(2048).decode()
        received_message = received_message.split("_", 1)[1] # return the data part of the message
        return received_message
