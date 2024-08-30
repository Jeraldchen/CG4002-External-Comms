import sys
from socket import *
import base64
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# test

def encrypt_and_encode_message(message):        
    secret_key = bytes('i_l0v3_CG4002_:D', 'utf-8')
    iv = Random.new().read(AES.block_size) # Random IV
    cipher = AES.new(secret_key, AES.MODE_CBC, iv) # AES CBC mode
    encrypted_message = message.encode('utf-8') # Encode message to bytes
    encrypted_message = cipher.encrypt(pad(encrypted_message, AES.block_size)) # Pad message and encrypt
    encoded_message = base64.b64encode(iv + encrypted_message) # Encode IV + encrypted message to base64

    return encoded_message

serverName = sys.argv[1]
serverPort = int(sys.argv[2])

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    message = "hello"
    encrypted_message = encrypt_and_encode_message(message)
    clientSocket.send(f"{len(encrypted_message)}_".encode()) # send in len(encrypted_message)_encrypted_message format
    clientSocket.send(encrypted_message)
    received_message = clientSocket.recv(2048)
    received_message = received_message.decode('utf-8')
    print(received_message)
