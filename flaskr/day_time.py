from datetime import datetime

# Example: String to datetime object
now = datetime.now()
now_str = now.strftime("%Y-%m-%d %H:%M:%S")
print("Current UTC Time:", now_str)
now2 = datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")
print("Current UTC Time:", now2)
