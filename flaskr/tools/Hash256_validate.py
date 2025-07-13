from Crypto.Hash import SHA256
import hashlib # python bultin lib

msg = 'First'
hash256 = SHA256.new(msg.encode())
# hash256.update('message')
digest = hash256.digest()
print("bin digest:", digest)
print("hex digest:", hash256.hexdigest())

print("is both libs hexdigest equal:",
      hash256.hexdigest() == hashlib.sha256(msg.encode()).hexdigest())

hash256_2 = SHA256.new(msg.encode())
print("is msg not change: ", digest == hash256_2.digest())

# --------- test from const--------------------
hash256 = SHA256.new(b'yaniv')
digest = hash256.hexdigest()
print("\nhex digest calc:", digest)
hexToValidate = "c7b18ad0447f947c2a4304951a624a599f61d66e1b62c36a43e4a4091e4e11c6"
print("hex digest orig:", hexToValidate)
print("hex digest valid:", digest == hexToValidate)
