import threading
import time
import logging
from typing import Any

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
lock = threading.Lock()
class massage:
    msg = None
    # Initializing
    def __init__(self, msg = None):
        self.msg = msg

    def setMsg(self, msg):
        self.msg = msg

    def getMsg(self) -> Any:
        return self.msg

def wait_for_event(event: threading.Event, msg: massage):
    for x in range(1, 5, 2): # x 1,3 in total loop 2 times
        logging.debug('wait_for_event starting')
        event_is_set = event.wait()
        event.clear()
        with lock:
            logging.debug('event set: %s, msg: %s' , event_is_set, msg.getMsg())

def wait_for_event_timeout(event: threading.Event, timeout, msg: massage):
    for x in range(4): # x from 0 to 3 in total loop 4 times
        #while not e.isSet():
        logging.debug('wait_for_event_timeout starting')
        event_is_set = event.wait(timeout)
        with lock:
            if event_is_set:
                logging.debug('event with timeout set: %s, msg: %s' , event_is_set, msg.getMsg())
                event.clear()
            else:
                logging.debug('Timeout Event doing other things')

if __name__ == '__main__':
    e = threading.Event()
    msg = massage()
    t1 = threading.Thread(name='blocking',
                      target=wait_for_event,
                      args=(e, msg))
    t1.start()

    t2 = threading.Thread(name='non-blocking',
                      target=wait_for_event_timeout,
                      args=(e, 2, msg))
    t2.start()

    logging.debug('Waiting before calling Event.set()')
    time.sleep(3)
    msg.setMsg("yaniv")
    e.set()
    logging.debug('Event is set')
    time.sleep(3)
    msg.setMsg("yaniv1")
    e.set()
    logging.debug('Event is set')
    time.sleep(3)
    t1.join() # wait for thread termination
    t2.join() # wait for thread termination
