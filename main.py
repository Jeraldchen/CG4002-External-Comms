import threading
from relay_node2.relay_server import RelayServer
from evaluation_client2.eval_client import EvalClient
import time

def start_relay_server(relay_server_port, eval_client_port):
    relay_server = RelayServer(relay_server_port, eval_client_port)
    relay_server.start_relay_server()

def start_eval_client(relay_server_port, eval_server_name, eval_server_port, eval_client_port):
    eval_client = EvalClient(relay_server_port, eval_server_name, eval_server_port, eval_client_port)
    eval_client.start_eval_client()

if __name__ == "__main__":
    relay_server_port = int(input("Enter the relay server port: "))
    eval_client_port = int(input("Enter the evaluation client port: "))
    eval_server_name = input("Enter the evaluation server name: ")
    eval_server_port = int(input("Enter the evaluation server port: "))  

    relay_server_thread = threading.Thread(target=start_relay_server, args=(relay_server_port, eval_client_port))
    eval_client_thread = threading.Thread(target=start_eval_client, args=(relay_server_port, eval_server_name, eval_server_port, eval_client_port))

    relay_server_thread.start()
    eval_client_thread.start()

    time.sleep(5) # wait for the relay server to start before sending the hello message

    relay_server_thread.join()
    eval_client_thread.join()