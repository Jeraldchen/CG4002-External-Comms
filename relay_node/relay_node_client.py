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
        