import base64
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class AESEncryption:
    def __init__(self):
        self.secret_key = bytes('i_l0v3_CG4002_:D', 'utf-8')


    def encrypt_and_encode_message(self, message):
        iv = Random.new().read(AES.block_size) # Random IV
        cipher = AES.new(self.secret_key, AES.MODE_CBC, iv) # AES CBC mode
        encrypted_message = message.encode('utf-8') # Encode message to bytes
        encrypted_message = cipher.encrypt(pad(encrypted_message, AES.block_size)) # Pad message and encrypt
        encoded_message = base64.b64encode(iv + encrypted_message) # Encode IV + encrypted message to base64

        return encoded_message