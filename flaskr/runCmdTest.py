import subprocess
import platform
import os
# result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE) # linux shell
# result = subprocess.run(['cmd', '/c', 'dir', 'C:\\Temp'], stdout=subprocess.PIPE) # windows cmd
# result = subprocess.run(['powershell', '/c', 'cat', 'setup.cfg'], stdout=subprocess.PIPE) # windows powershell

# for multiplatform run cmd.sh that contain #!/bin/bash ls -s"
# need in linux to "chmod u+x script.sh"
cwd = os.getcwd() # currect working dir
print(cwd)
if  platform.system() != "Windows":
    result = subprocess.run(['sh ./flaskr/cmd.sh', '/c/Temp'], stdout=subprocess.PIPE, shell=True, text=True, check=False)
else :
    result = subprocess.run(['sh', './flaskr/cmd1.sh', '/c/Temp'], stdout=subprocess.PIPE, shell=True, text=True, check=False)
if result.returncode == 0:
    print(result.stdout.decode('utf-8'))
else:
    print("error occurred")

# capture the error masg or print the output in no error
param = "-n" if platform.system() == "Windows" else "-c"
hostname = "8.8.8.8"  # Google's DNS server
# hostname = "8.8.8.81"
ERROR = True
try:
    result = subprocess.run( ["ping", hostname, param, "1"], check=True, capture_output=True, text=True)
    ERROR = False
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Command '{e.cmd}' failed with return code {e.returncode}")
    print(f"Error message: {e.output}")
except Exception as e:
    # print(f"Command '{e.cmd}' failed with return code {e.returncode}")
    print(f"Error message: {repr(e)}")

print(f"internet is {'not ' if ERROR else ''}live")
