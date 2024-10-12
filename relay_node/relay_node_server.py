from socket import *
from multiprocessing import *
from colours.colours import Colours
import json

class RelayNodeServer:
    def __init__(self, server_port):
        self.server_port = server_port
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Allow address reuse
        self.server_socket.bind(('', server_port))
        self.server_socket.listen()
        print('The relay node server is ready to receive messages')

    def receive_message(self, connection_socket):
        data = b'' # receive len followed by _ and then the data
        while not data.endswith(b'_'):
            _d = connection_socket.recv(1)
            if not _d:
                data = b''
                break
            data += _d
        data = data.decode()
        length = int(data[:-1]) # exclude the last character which is _ to just get the length

        data = b''
        while len(data) < length:
            _d = connection_socket.recv(length - len(data))
            if not _d:
                data = b''
                break
            data += _d

        return data

    def handle_client(self, connection_socket, client_addr, to_ai_queue: Queue, from_eval_server: Queue):
        while True:
            print('Connection from', client_addr)
            try:
                while True: # receive messages from the client
                    data = self.receive_message(connection_socket)
                    message = data.decode()
                    message_json = json.loads(message)
                    if message_json["packet_type"] == "M":
                        to_ai_queue.put(message_json) # send the IMU data packet to the AI   
                    # print('Received:', message + ' from ' + str(client_addr))
                    print(f"{Colours.CYAN}Received: {message} from {str(client_addr)}{Colours.RESET}")
                    print(f'{Colours.CYAN}###############################################{Colours.RESET}')
                    try:
                        true_game_state = from_eval_server.get() # get the message from the game engine
                    except Exception as e:
                        print(f"Error while getting message from eval server queue: {e}")
                        break

                    connection_socket.send(f"{len(true_game_state)}_{true_game_state}".encode()) # send the message back to the relay client
                    # connection_socket.send(f"{len(message)}_{message}".encode()) # send the message back to the client for confirmation
            except Exception as e:
                print('Error:', e)
            finally:
                connection_socket.close()
                print(f"Connection closed from {client_addr}")
    
    def run(self, to_ai_queue: Queue, from_eval_server: Queue):
        while True:
            connection_socket, client_addr = self.server_socket.accept()
            client_process = Process(target=self.handle_client, args=(connection_socket, client_addr, to_ai_queue, from_eval_server))
            client_process.start()
                