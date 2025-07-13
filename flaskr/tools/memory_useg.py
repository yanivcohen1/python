import time
import os
import psutil


def memory_usage():
    process = psutil.Process(os.getpid()) # rss (Resident Set Size) not include vistual memory
    return process.memory_info().rss / (1024 * 1024)


print(f'memory useg: {memory_usage():.2f} MB') # matches “Mem Usage” column of taskmgr.exe.
