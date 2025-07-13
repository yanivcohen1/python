import base64
# Crypto use lib pycryptodome
# https://www.javainuse.com/aesgenerator
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 32 # Bytes (msg long for ascii)

# Generate a random key
key = get_random_bytes(16)  # AES128 key size is 16 bytes or 128 bits
key = b"aesEncryptionKey"
print("key:", key)
str1 =  base64.b64encode(key).decode()
print("key base64:", str1)
print("key:", base64.b64decode(str1.encode()))
print()

# Setup cipher
# cipher = AES.new(key, AES.MODE_EAX)  # EAX mode is recommended for new applications
# iv = cipher.nonce
iv = b"aesEncryption_IV"
print("IV-Initialization Vector:", iv)
print()

# Encrypt data
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
data = b'Your data to encrypt'
print("msg to encrypt:", data)
# data += b' ' * (16 - len(data) % 16)  # Padding to ensure correct block size
data = pad(data, AES.block_size) # round to the neerest multiple of 16 bit with padding
ciphertext = cipher.encrypt(data)
print("encrypt msg:", ciphertext.hex())
ciphertext_b64 =  base64.b64encode(ciphertext).decode()
print("encrypt msg base64:", ciphertext_b64)

# Decrypt data
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
plaintext = cipher.decrypt(ciphertext)
# print("decrypt msg:", plaintext.rstrip())
print("decrypt msg:", unpad(plaintext, AES.block_size).decode('utf-8')) # remove the pedding

num_padding_bytes = plaintext[-1]
print("BLOCK_SIZE:", num_padding_bytes )
