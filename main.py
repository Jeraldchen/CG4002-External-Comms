import sys
from encryption import AESEncryption
from evaluation_client import EvaluationClient

if __name__ == "__main__":
    server_name = sys.argv[1]
    server_port = int(sys.argv[2])
    
    client = EvaluationClient(server_name, server_port)
    client.hello()