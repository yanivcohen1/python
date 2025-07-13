import win32file
import win32event
import win32con

times = 0
# Directory to monitor
path_to_watch = "D:\\Temp\\unity" # "C:\\path\\to\\directory"

# Create a handle for the directory
change_handle = win32file.FindFirstChangeNotification(
    path_to_watch,
    0,
    win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
    win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
    win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
    win32con.FILE_NOTIFY_CHANGE_SIZE |
    win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
    win32con.FILE_NOTIFY_CHANGE_SECURITY
)

try:
    while True:
        # Wait for a change to occur
        result = win32event.WaitForSingleObject(change_handle, win32event.INFINITE)

        if result == win32con.WAIT_OBJECT_0:
            if times == 0:
                times += 1
                print("Change detected in directory:", path_to_watch)
            else:
                times = 0
            # Reset the change notification handle
            win32file.FindNextChangeNotification(change_handle)

        else:
            print("Failed to wait for directory change.")
            break
finally:
    win32file.FindCloseChangeNotification(change_handle)
