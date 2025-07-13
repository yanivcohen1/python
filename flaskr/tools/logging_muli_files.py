import socket
import time
import logging
from logging.handlers import RotatingFileHandler
# Set up logging
# logging.basicConfig(filename='connection_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# https://stackoverflow.com/questions/24505145/how-to-limit-log-file-size-in-python
app_log = logging.getLogger('root')

def init_logger():
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

    logFile = 'D:\\Temp\\log\\log' # connection_log.txt

    my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024,
                                    backupCount=2, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)

    app_log.setLevel(logging.INFO)

    app_log.addHandler(my_handler)


def is_connected():
    try:
        # Connect to a well-known host (Google DNS server)
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False

def log_status(status):
    # timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{'Online' if status else 'Offline'}"
    if status:
        app_log.info(log_entry)
    else:
        app_log.error("Alert: Internet connection is offline!")

def main():
    while True:
        status = is_connected()
        log_status(status)
        if not status:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"{timestamp} - Alert: Internet connection is offline!")
        time.sleep(7)  # Check every 60 seconds

if __name__ == "__main__":
    init_logger()
    main()
