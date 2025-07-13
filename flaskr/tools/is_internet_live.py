import subprocess
import platform

# hostname = "google.com" #example
param = "-n" if platform.system() == "Windows" else "-c"
hostname = "8.8.8.8"  # Google's DNS server
# hostname = "8.8.8.81"
ERROR = True
try:
    result = subprocess.run( ["ping", hostname, param, "1"], check=True, capture_output=True, text=True)
    ERROR = False
    # print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Command '{e.cmd}' failed with return code {e.returncode}")
    print(f"Error message: {e.output}")
except Exception as e:
    # print(f"Command '{e.cmd}' failed with return code {e.returncode}")
    print(f"Error message: {repr(e)}")

print(f"internet is {'not ' if ERROR else ''}live")
