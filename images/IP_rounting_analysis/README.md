### Intruction:
Create a Python script using PyBGPStream to monitor real-time (project='ris-live') BGP updates, focusing on announcements from AS6830. The script utilizes a dictionary to track the timestamp and count of announcements for each prefix associated with AS6830. Implement a function that checks daily if the data needs to be reset by comparing the current date with the date of the last reset, and if they differ, it clears the dictionary, ensuring data freshness each new day. The script should also alert if any prefix's count exceeds 10,000 to flag significant anomalies in real time. For extracting AS paths from BGP updates, use the code as_path = elem.fields.get('as-path', '').split() to accurately parse the path and identify announcements directly associated with AS6830. This setup enables ongoing, dynamic monitoring and analysis of BGP path announcements, crucial for network stability and security oversight.

### Code output:
```python
import pybgpstream
import datetime

# Initialize BGPStream for real-time monitoring
stream = pybgpstream.BGPStream(
    project="ris-live",
    record_type="updates",
)

# Initialize a dictionary to store the time-series data
time_series_data = {}

# Function to reset data daily
def reset_daily(last_reset):
    if datetime.datetime.now().date() > last_reset.date():
        return True
    return False

# Track the last reset time
last_reset_time = datetime.datetime.now()

# Loop through the stream records continuously as they arrive in real-time
for rec in stream.records():
    # Check if a reset is needed
    if reset_daily(last_reset_time):
        time_series_data = {}
        last_reset_time = datetime.datetime.now()
        print("Data has been reset for the new day.")

    for elem in rec:
        if elem.type == "A":  # Analyze only BGP announcements
            as_path = elem.fields.get('as-path', '').split()
            origin_as = as_path[0]
            if origin_as == "6830":
                prefix = elem.fields["prefix"]
                time_str = datetime.datetime.fromtimestamp(rec.time).strftime('%Y-%m-%d %H:%M:%S')
                # Construct key to include time
                key = (prefix, time_str)
                if key not in time_series_data:
                    time_series_data[key] = 1  # Initialize the count for the prefix
                else:
                    time_series_data[key] += 1  # Increment the count for the prefix
                    # Check if the count exceeds 10,000
                    if time_series_data[key] > 10000:
                        print(f"Alert: Count for {key} has exceeded 10,000.")

                print("Current time-series data for AS 6830:")
                for key, count in sorted(time_series_data.items()):
                    print(f"Prefix: {key[0]}, Time: {key[1]}, Count: {count}")
```