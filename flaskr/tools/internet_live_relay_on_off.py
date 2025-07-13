# https://github.com/JPEWdev/pyhid-usb-relay
# hid - human interface device
# #! /usr/bin/env python3
import time
from enum import Enum
import socket
import logging
from logging.handlers import RotatingFileHandler
import pyhid_usb_relay
# Set up logging
# logging.basicConfig(filename='connection_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

app_log = logging.getLogger('root')
# https://stackoverflow.com/questions/24505145/how-to-limit-log-file-size-in-python
def config_log_file():
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

    logFile = 'connection_log' # 'D:\\Temp\\log\\log' # connection_log

    my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024,
                                    backupCount=2, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)

    app_log.setLevel(logging.INFO)
    app_log.addHandler(my_handler)

# while True:
#     app_log.info("data")
class Devices(Enum):
    RELAY_1 = 1
    RELAY_2 = 2

relay = None
try:
    relay = pyhid_usb_relay.find()
    print("relay serial:", relay.serial)
    # Example of reading state and toggling relay #1
    print(
        f"{Devices.RELAY_1.name} is",
        "on" if relay.get_state(Devices.RELAY_1.value) else "off",
    )
except Exception as e:
    app_log.error("relay exception:" + str(e))
    print("relay error:", e)

def off_on_relay():
    try:
        relay.toggle_state(Devices.RELAY_1.value)
        print(
            f"{Devices.RELAY_1.name} after toggle is",
            'on' if relay.get_state(Devices.RELAY_1.value) else 'off',
        )
        time.sleep(10)
        relay.toggle_state(Devices.RELAY_1.value)
        print(
            f"{Devices.RELAY_1.name} after toggle is",
            'on' if relay.get_state(Devices.RELAY_1.value) else 'off',
        )
    except Exception as e:
        app_log.error("relay exception:" + str(e))
        print("relay error:", e)


def is_connected():
    try:
        # Connect to a well-known host (Google DNS server)
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False

def log_status(status):
    if status:
        app_log.info("Online")
    else:
        app_log.error("Alert: Internet connection is offline!")

def main():
    while True:
        status = is_connected()
        log_status(status)
        if not status:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"{timestamp} - Alert: Internet connection is offline!")
            off_on_relay()
            time.sleep(180) # wait 180 sec - 3 min + 1 min for main loop = 4 min
        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    config_log_file()
    main()
