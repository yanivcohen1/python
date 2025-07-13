import threading
import time
import logging

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

    def getMsg(self) -> any:
        return self.msg

def consumer(condition: threading.Condition ,msg: massage, timeout = None):
    for x in range(1, 5, 2): # 1, 3 Loop twice in total
        logging.debug('Consumer waiting ...')
        is_time_out = False
        with condition:
            is_time_out = condition.wait(timeout)
        with lock:
            logging.debug('Consumer consumed the resource, set timeout: %s, msg %s, timeOut %s', 
                timeout, msg.getMsg(), not is_time_out)

def producer(condition: threading.Condition, msg: massage):
    msg.setMsg("from producer thread")
    logging.debug('Notifying to all consumers, msg %s', msg.getMsg())
    with condition:
        condition.notifyAll()

if __name__ == '__main__':
    condition = threading.Condition()
    msg = massage()
    cs1 = threading.Thread(name='consumer1', target=consumer, args=(condition, msg))
    cs2 = threading.Thread(name='consumer2', target=consumer, args=(condition, msg, 3)) # timeout 3 sec
    pd = threading.Thread(name='producer', target=producer, args=(condition, msg))

    cs1.start()
    time.sleep(2)
    cs2.start()
    time.sleep(2)
    msg.setMsg("from main thread")
    with condition:
        condition.notify_all()
    time.sleep(4)
    pd.start()
    pd.join() # wait for thread termination
    cs1.join() # wait for thread termination
    cs2.join() # wait for thread termination