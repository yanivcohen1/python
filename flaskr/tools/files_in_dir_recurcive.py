import os

DOWMLOAD_DIR = "D:\\Temp\\esp32-multi-tasking\\src"
for (dirpath, dirnames, filenames) in os.walk(DOWMLOAD_DIR):
    for filename in filenames:
        print(dirpath + "\\" + filename)
