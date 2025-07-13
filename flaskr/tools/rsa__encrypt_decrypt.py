import rsa
import base64
import pickle

# Generate a new RSA key pair of 2048 bits
public_key, private_key = rsa.newkeys(2048)

def load_public_key_openssl_pem(pub_key_string: str):
    return rsa.PublicKey.load_pkcs1_openssl_pem(pub_key_string.encode())

def load_public_key_pem(pub_key_string: str):
    return rsa.PublicKey.load_pkcs1(pub_key_string.encode(), "PEM")

pem_rsa_pub_key_pem = public_key.save_pkcs1("PEM")
# Convert to OpenSSL-compatible PEM format
# openssl rsa -pubin -in rsa_public_key.pem -RSAPublicKey_out -out rsa_openssl_public_key.pem

print("publicKeyPem:", pem_rsa_pub_key_pem)
public_key = load_public_key_pem(pem_rsa_pub_key_pem.decode())
print("publicKey:", public_key)


# Encrypt a message with the public key
message = 'This is a secret message.'
serialize_msg = pickle.dumps(message)
encrypted_message = rsa.encrypt(serialize_msg, public_key)

# Decrypt the message with the private key
decrypted_message = rsa.decrypt(encrypted_message, private_key)

print(f'Original message: {message}')
print(f'Encrypted message: {base64.b64encode(encrypted_message)}')
print(f'Decrypted message: {pickle.loads(decrypted_message)}')
