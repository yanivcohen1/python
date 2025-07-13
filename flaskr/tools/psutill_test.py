import psutil
psutil.test()

# prints like windosw task manager:
# USER         PID  %MEM     VSZ     RSS  NICE STATUS  START   TIME  CMDLINE
# SYSTEM         0   0.0   60.0K    8.0K        runni         56:19  System Idle Process
# SYSTEM         4   0.0   72.0K    7.2M        runni         56:42  System
#              204   0.2  184.0K  148.2M        stopp  Jan15  00:00
#              236   0.1   32.5M   43.2M        runni  Jan15  00:17  Registry
# yaniv        492   0.0    1.3M    6.3M    32  runni  Feb01  00:00  \\?\C:\WINDOWS\system32\conhost.exe --headless --width 80 --height 30 --signal 0xa38 --server 0x524
