import os

currentDir = os.path.join(os.path.dirname(__file__))
print("current dir:", currentDir) # c:\Users\yaniv\OneDrive\python-flask\flaskr\tools
print('current file name:', os.path.basename(__file__)) # current_dir.py
reletive_file_path = "/../dst/target_2.txt"
full_file_path = str(currentDir) + reletive_file_path
print('full file path:    ',os.path.normpath(full_file_path))

# for parent dir
target_path_2 = os.path.join(currentDir, '../dst/target_2.txt')
print('normalize    : ', os.path.normpath(target_path_2))
print('file name:    ', os.path.basename(target_path_2))
