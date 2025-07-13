import base64
# Crypto use lib pycryptodome
# https://www.javainuse.com/aesgenerator
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Generate a random key
key = get_random_bytes(16)  # AES128 key size is 16 bytes or 128 bits
print("key:", key)
str1 =  base64.b64encode(key).decode()
print("key base64:", str1)
print("key:", base64.b64decode(str1.encode()))
print()

# Setup cipher
cipher = AES.new(key, AES.MODE_EAX)  # EAX mode is recommended for new applications
nonce = cipher.nonce
print("IV-Initialization Vector:", nonce)
print()

# Encrypt data
data = b'Your data to encrypt'
print("msg to encrypt:", data)
ciphertext, tag = cipher.encrypt_and_digest(data)
print("encrypt msg:", ciphertext)

# Decrypt data
cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
plaintext = cipher.decrypt(ciphertext)
print("decrypt msg:", plaintext)

# Verify if the data was not tampered with
try:
    cipher.verify(tag)
    print("The message is authentic:", plaintext)
except ValueError:
    print("Key incorrect or message corrupted")
