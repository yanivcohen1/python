import os
import yaml

currentDir = os.path.join(os.path.dirname(__file__))
with open(currentDir + '/config_dev.yml', 'r') as file:
    prime_service_dict = yaml.safe_load(file)

print(prime_service_dict['rest']['url']) # https://example.org/primenumbers/v1
port = prime_service_dict['rest']['port']
print(port) # 8443
print(type(port) is int) # <class 'int'>
