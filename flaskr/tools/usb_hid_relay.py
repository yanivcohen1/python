# https://github.com/JPEWdev/pyhid-usb-relay
# hid - human interface device
# #! /usr/bin/env python3
import time
from enum import Enum
import pyhid_usb_relay

class Devices(Enum):
    RELAY_1 = 1
    RELAY_2 = 2

if __name__ == "__main__":
    relay = pyhid_usb_relay.find()
    print(relay.serial)
    # Example of reading state and toggling relay #1
    print(f"{Devices.RELAY_1.name} is", relay.get_state(Devices.RELAY_1.value))
    if relay.get_state(Devices.RELAY_1.value):
        relay.toggle_state(Devices.RELAY_1.value)
        time.sleep(3)
        print(f"{Devices.RELAY_1.name} after toggle is", relay.get_state(Devices.RELAY_1.value))

    if not relay.get_state(Devices.RELAY_1.value):
        relay.toggle_state(Devices.RELAY_1.value)
        time.sleep(3)
        print(f"{Devices.RELAY_1.name} after toggle is", relay.get_state(Devices.RELAY_1.value))

    # # You can also refer to relays by index
    # if relay[1]:
    #     relay[1] = False
    # time.sleep(3)

    # if not relay[1]:
    #     relay[1] = True
    # time.sleep(3)

    # # If you have relay aliases defined in your config file, you can also refer
    # # to them in place of the index:
    # relay["relay1"] = not relay["relay1"] # raspberrypi4
