import subprocess
import platform

hostname = "8.8.8.8"
count_param = "-n" if platform.system().lower() == "windows" else "-c"

# Use subprocess.Popen to stream output in real-time
with subprocess.Popen(["ping", count_param, "3", hostname], stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, text=True, bufsize=1) as process:
    for line in process.stdout:
        print(line, end="")  # Print each line as it arrives

if process.returncode != 0:
    print(f"\nProcess finished with return code {process.returncode}")
