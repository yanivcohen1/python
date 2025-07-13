import codecs

# for strings
message = "HeyK"
message_as_bytes = message.encode()
print(type(message_as_bytes)) #see the printed type
print(type(b'this is a message2'))
message_as_hex = message_as_bytes.hex()
print(message_as_hex)
my_bytes = bytes.fromhex(message_as_hex)
print(my_bytes.decode())
print(codecs.decode(message_as_hex, 'hex').decode("ASCII")) # generic

import base64
# for base64
message_as_base64_bytes = base64.b64encode(message_as_bytes)
print(message_as_base64_bytes.decode())
message_as_ascii_bytes = base64.b64decode(message_as_base64_bytes.decode())
print(message_as_ascii_bytes.decode())

num = 1563
intBytes = num.to_bytes(4, "big")
base64Str = base64.urlsafe_b64encode(intBytes)
base64Int = base64.urlsafe_b64decode(base64Str)
num2 = int.from_bytes(base64Int, "big")
print(f"convert {num}: to b64 str {base64Str.decode()[:-2]} and return to: {num2} is pass: {num==num2}")

# for numbers
print(0x1A)   # Print the decimal value of the hexadecimal number after the “0x”
print(hex(123)) # Prints the hexadecimal value of the number 123
print(bin(123)) # Prints the binary string of the number 123
print(int("1010", 2)) # Prints the decimal value of the number 1010 (base 2)
print(int("1A1B", 16)) # Prints the decimal value of the number 1A1B (base 16)
number_as_bytes = int.to_bytes(515, 2, byteorder='big') # bigger number firsst
number = int.from_bytes(number_as_bytes, byteorder='big')
print(number)
print(int(bytes.hex(number_as_bytes), 16))

# open binary file
file_name = "C:\\Temp\\Adi\\adi\\first_year\\Week25\\command1.bin"
file = open(file_name, "rb")
lines = file.readlines()
print(lines[0])
file.close()

# test
msg = "0a1111115155524e535534675156565553475a6b4a444d734e413d3d"
msg = "0811111164584e6c636941784d6a4e6863444641"
my_bytes = bytes.fromhex(msg)
print(my_bytes.decode())
# import base64
# number = int.from_bytes(bytes.fromhex(msg[:2]), byteorder='big')
message_as_base64_bytes = base64.b64decode(my_bytes)[:int(msg[:2], 16)]
print(message_as_base64_bytes.decode())
