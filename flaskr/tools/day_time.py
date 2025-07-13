from datetime import datetime, timedelta

# Get the current date and time
now = datetime.now()

# Add one day and one minute
new_time = now + timedelta(days=1, minutes=1)

# Print the new date and time
print("Current date and time:", now)
print("New date and time:", new_time)
print("format Current date and time:", now.strftime("%d/%m/%Y %H:%M:%S"))
print(
  f"{now.day:2.0f}/{now.month:2.0f}/{now.year} {now.hour:2.0f}:{now.minute:2.0f}:{now.second:2.0f}"
)
