from socket import *

class RelayNodeServer:
    def __init__(self, server_port):
        self.server_port = server_port
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(('', server_port))
        self.server_socket.listen()
        print('The relay node server is ready to receive messages')

    def run(self):
        while True:
            connection_socket, client_addr = self.server_socket.accept()
            print('Connection from', client_addr)
            try:
                while True:
                    message = connection_socket.recv(2048)
                    received_message = message.decode().split("_", 1)[1]
                    if not message:
                        break
                    print('Received:', received_message + ' from ' + str(client_addr))
                    connection_socket.send(message)
                connection_socket.close()
            except Exception as e:
                print('Error:', e)
                connection_socket.close()
                break