from datetime import datetime, timezone, timedelta

# Specify the date and time
target_date_time_str = "2023-09-15T08:00:00Z"

# Convert the string to a datetime object
target_date_time = datetime.strptime(target_date_time_str, "%Y-%m-%dT%H:%M:%SZ")



# Optionally, you can set the timezone to UTC
target_date_time_utc = target_date_time.replace(tzinfo=timezone.utc)
current_datetime = datetime.now()
formatted_date_time = target_date_time_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
formatted_date_time_curr = current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
print(formatted_date_time)
print(formatted_date_time_curr)