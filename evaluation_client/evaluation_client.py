from socket import *
from evaluation_client.encryption import AESEncryption

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
        data = b'' # receive len followed by _ and then the data
        while not data.endswith(b'_'):
            _d = self.socket.recv(1)
            if not _d:
                data = b''
                break
            data += _d
        data = data.decode()
        length = int(data[:-1]) # exclude the last character which is _ to just get the length

        data = b''
        while len(data) < length:
            _d = self.socket.recv(length - len(data))
            if not _d:
                data = b''
                break
            data += _d
        
        return data.decode()

        
                
            
            
