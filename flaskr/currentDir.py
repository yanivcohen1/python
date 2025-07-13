import os
from pathlib import Path

currentDir = os.path.join(os.path.dirname(__file__))
print("current dir:", currentDir) # c:\Users\yaniv\OneDrive\python-flask\flaskr
print('current file name:', os.path.basename(__file__)) # currentDir.py
reletive_file_path = "/../dst/target_2.txt"
full_file_path = currentDir + reletive_file_path
print('full file path:    ',os.path.normpath(full_file_path))
# full file path:     c:\Users\yaniv\OneDrive\python-flask\dst\target_2.txt
print('from reletive path:    ',os.path.abspath('./flaskr/'))
# from reletive path:     C:\Users\yaniv\OneDrive\python-flask\flaskr

# for parent dir
target_path_2 = os.path.join(currentDir, '../dst/target_2.txt')
print('normalize    : ', os.path.normpath(target_path_2))
print('file name:    ', os.path.basename(target_path_2))


print(os.__file__) # tells you where the os module is for current python path

cwd_module = os.getcwd()
print(cwd_module) # C:\Users\yaniv\OneDrive\python-flask

current_directory = os.path.dirname(__file__)
print(current_directory)

absolute_path = str(Path(__file__).parent.resolve())
print(absolute_path) # C:\Users\yaniv\OneDrive\python-flask\flaskr

# for multi win and linux add path
print(Path(absolute_path + "/cmd.sh").is_file()) # true
reletive_path = 'flaskr/cmd.sh'
print(Path(reletive_path).is_file()) # true

path = Path('./')
print(path.resolve()) # C:\Users\yaniv\OneDrive\python-flask
new_path = path.resolve() / 'flaskr' / 'currentDir.py'
print(new_path.resolve()) # C:\Users\yaniv\OneDrive\python-flask\flaskr\currentDir.py
print(new_path.exists()) # True
print(new_path.is_dir()) # False
with new_path.open() as f: print(f.readline()) # print - import os

# ---------- recorcive on folder tree ------
from os import walk

f = []
d = []
mypath = os.getcwd()
for (dirpath, dirnames, filenames) in walk(mypath):
    print("In the Directory:", dirpath)
    f.extend(filenames) # all files in this dir
    d.extend(dirnames) # all directoris in this dir
    break # only top level not recorsie - remove this for recorsive
print("\nare Files:", f)
print("\nare Folders:", d)
