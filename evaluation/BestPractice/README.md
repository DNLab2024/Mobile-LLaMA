# Code examples generated by Mobile-LLaMA, LLaMA-13B, GPT-3.5 (October 2023)

## Intruction:
Create a Python script using PyBGPStream to monitor real-time (project='ris-live') BGP updates, focusing on announcements from AS6830. The script utilizes a dictionary to track the timestamp and count of announcements for each prefix associated with AS6830. Implement a function that checks daily if the data needs to be reset by comparing the current date with the date of the last reset, and if they differ, it clears the dictionary, ensuring data freshness each new day. The script should also alert if any prefix's count exceeds 10,000 to flag significant anomalies in real time. For extracting AS paths from BGP updates, use the code as_path = elem.fields.get('as-path', '').split() to accurately parse the path and identify announcements directly associated with AS6830.

### Mobile-LLaMA code output:
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

### Mobile-LLaMA code output results:
```plaintext
Current time-series data for AS 6830:
Prefix: 103.191.181.0/24, Time: 2024-04-30 11:05:28, Count: 1
Prefix: 103.90.13.0/24, Time: 2024-04-30 11:05:28, Count: 1
Prefix: 196.43.131.0/24, Time: 2024-04-30 11:05:28, Count: 1
Prefix: 209.22.66.0/24, Time: 2024-04-30 11:05:28, Count: 2
Prefix: 209.22.67.0/24, Time: 2024-04-30 11:05:28, Count: 2
Prefix: 2600:40fc:1004::/48, Time: 2024-04-30 11:05:28, Count: 2
Prefix: 2600:40fc:1004::/48, Time: 2024-04-30 11:05:29, Count: 1
Prefix: 2605:9cc0:c0f::/48, Time: 2024-04-30 11:05:28, Count: 2
Prefix: 2804:31c4::/32, Time: 2024-04-30 11:05:29, Count: 1
Prefix: 2806:20d:3600::/40, Time: 2024-04-30 11:05:28, Count: 1
Prefix: 2806:20d:3600::/40, Time: 2024-04-30 11:05:29, Count: 2
...
```

### GPT-3.5 code output:
Comments: 
- Incorrect use of `filter` parameter
- Invalid code output

```python
import pybgpstream
from datetime import datetime, timedelta

as6830_prefixes = {}
last_reset_date = datetime.now().date()

def reset_data_if_needed():
    global last_reset_date
    current_date = datetime.now().date()
    if current_date != last_reset_date:
        as6830_prefixes.clear()
        last_reset_date = current_date
        print("Data reset at", datetime.now())

def process_bgp_update(elem):
    global as6830_prefixes
    prefix = elem.fields['prefix']
    timestamp = elem.time
    if prefix in as6830_prefixes:
        as6830_prefixes[prefix]['count'] += 1
    else:
        as6830_prefixes[prefix] = {'count': 1, 'timestamp': timestamp}
    print("Update for prefix", prefix, "from AS6830 at", datetime.fromtimestamp(timestamp))
    # Check for anomalies
    if as6830_prefixes[prefix]['count'] > 10000:
        print("Anomaly detected for prefix", prefix, "from AS6830!")
        # You can add additional actions/alerts here

def run_monitor():
    stream = pybgpstream.BGPStream(
        from_time=datetime.now() - timedelta(minutes=5),
        until_time=datetime.now(),
    )

    # Set the filter for the RRC15 collector
    stream.add_project="ris-live",
    stread.add_filter="prefix more 0 and type ribs and collector route-views2 and peer 6830"

    for elem in stream:
        process_bgp_update(elem)
        reset_data_if_needed()

run_monitor()
```

### LLaMA 13B code output:
Comments: 
- Incorrect use of PyBGPStream library - Hallucination

```python
import pybgpstream
import datetime

# Set up the PyBGPStream connection
stream = pybgpstream.BGPStream('ris-live')

# Define the dictionary to track the timestamp and count of announcements for each prefix associated with AS6830
as6830_prefixes = {}

# Define the function to check if the data needs to be reset daily
def reset_data():
    today = datetime.date.today()
    if today!= as6830_prefixes['last_reset']:
        as6830_prefixes = {}
        as6830_prefixes['last_reset'] = today

# Define the function to alert if any prefix's count exceeds 10,000
def alert_if_anomaly():
    for prefix, count in as6830_prefixes.items():
        if count > 10000:
            print(f"Anomaly detected: {prefix} count exceeds 10,000")

# Loop over the BGP updates and extract the AS path for each update
for update in stream:
    # Extract the AS path from the update
    as_path = update.fields.get('as-path', '').split()
    if as_path and as_path[0] == 'AS6830':
        # Increment the count of prefixes associated with AS6830
        prefix = as_path[1]
        if prefix not in as6830_prefixes:
            as6830_prefixes[prefix] = 1
        else:
            as6830_prefixes[prefix] += 1

# Reset the data daily
reset_data()

# Alert if any prefix's count exceeds 10,000
alert_if_anomaly()
```