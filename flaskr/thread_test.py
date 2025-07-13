import logging
import threading
import time
import random

lock = threading.Lock()

class Pipeline:
    """
    Class to allow a single element pipeline between producer and consumer.
    """
    def __init__(self):
        self.message = ""
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()

    def get_message(self):
        #self.consumer_lock.acquire()
        message = self.message
        #self.producer_lock.release()
        return message

    def set_message(self, message):
        #self.producer_lock.acquire()
        self.message = message
        #self.consumer_lock.release()

def thread_function(pipeline):
    logging.info("Thread " + pipeline.get_message() + ": starting")
    msg = pipeline.get_message() #local no need lock
    pipeline.set_message(msg + " thread added")
    lock.acquire()
    logging.info("this is safe zone")
    lock.release()
    time.sleep(2)
    logging.info("Thread " + pipeline.get_message() + " finishing")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    threads = list(threading.Thread)
    pipeline = Pipeline()
    pipeline.set_message("init msg")
    x = threading.Thread(target=thread_function, args=(pipeline, ))
    pipeline2 = Pipeline()
    pipeline2.set_message("init msg2")
    x2 = threading.Thread(target=thread_function, args=(pipeline2, ))
    threads.append(x)
    threads.append(x2)
    logging.info("Main    : before running thread")
    x.start()
    x2.start()
    logging.info("Main    : wait for the thread to finish")
    #x.join()
    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join() # wait for thread termination
        logging.info("Main    : thread %d done", index)

    logging.info("massage read: " + pipeline.get_message())
    logging.info("massage2 read: " + pipeline2.get_message())
    logging.info("Main    : all done")