from datetime import datetime, timedelta

# from time import gmtime, strftime
import time


def time_and_date_localization():
    """Calculate the time and date

    Returns:
        str: time and date
    """
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")  # 29/06/2023 18:20:49
    gmt = time.gmtime()
    print(
        "\nLocal: " + now.strftime("%a, %d %b %Y %I:%M:%S %p %Z")
    )  # Local: Mon, 08 May 2017 11:51:07 AM IST
    print(
        "\nGMT: " + time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmt)
    )  # GMT: Mon, 08 May 2017 06:21:07 AM GMT
    print("\nYour Time Zone is GMT", time.strftime("%z", gmt))
      # Your Time Zone is GMT +0200
    return dt_string

# Example: String to datetime object
now = datetime.now()
now_str = now.strftime("%Y-%m-%d %H:%M:%S")
print("Current UTC Time:", now_str)
now2 = datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")
print("Current UTC Time:", now2)

time_and_date_localization()

# timeDate menipulation
date_string = "2022-03-19 17:01:37"
date_format = "%Y-%m-%d %H:%M:%S"
# Convert string to datetime
endDate = datetime.strptime(date_string, date_format)
# date_time_str = dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
startDate = endDate - timedelta(days=18) # reduce from todaty 18 days
print("delta time is:", startDate) # 2022-03-01 17:01:37
