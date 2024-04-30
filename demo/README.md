# Demonstrations of Mobile-LLaMA's capabilities: IP routing analysis, Packet analysis, Performance analysis

## IP routing analysis
Perform BGP analysis using PyBGPStream and detect anomalies in AS path lengths for IPv4 prefixes over two time periods: from January 15, 2023, 15:00 to January 15, 2023, 17:00.
```python
import pybgpstream
from collections import defaultdict

# Initialize BGPStream instance
stream = pybgpstream.BGPStream(
    from_time="2023-01-15 15:00:00",
    until_time="2023-01-15 17:00:00",
    filter="ipversion 4",
    record_type="updates",
)

# Dictionary to store AS path lengths
as_path_lengths = defaultdict(int)

# Process BGP records
for rec in stream.records():
    for elem in rec:
        as_path = elem.fields.get('as-path', '').split()
        prefix = elem.fields["prefix"]

        # Update AS path lengths
        as_path_lengths[prefix] = max(as_path_lengths[prefix], len(as_path))

# Calculate mean AS path length
mean_length = sum(as_path_lengths.values()) / len(as_path_lengths)

# Detect anomalies
anomalies = [prefix for prefix, length in as_path_lengths.items() if length > mean_length * 2]

print("Anomalies detected from 2023-01-15 15:00:00 to 2023-01-15 17:00:00:")
if anomalies:
    for prefix in anomalies:
        print(f"Prefix: {prefix}, AS Path Length: {as_path_lengths[prefix]}")
else:
    print("No anomalies detected.")

# Initialize BGPStream instance for the second time period
stream = pybgpstream.BGPStream(
    from_time="2023-01-18 12:00:00",
    until_time="2023-01-18 13:00:00",
    filter="ipversion 4",
    record_type="updates",
)

# Reset AS path lengths dictionary
as_path_lengths = defaultdict(int)

# Process BGP records
for rec in stream.records():
    for elem in rec:
        as_path = elem.fields.get('as-path', '').split()
        prefix = elem.fields['prefix']

        # Update AS path lengths
        as_path_lengths[prefix] = max(as_path_lengths[prefix], len(as_path))

# Calculate mean AS path length
mean_length = sum(as_path_lengths.values()) / len(as_path_lengths)

# Detect anomalies
anomalies = [prefix for prefix, length in as_path_lengths.items() if length > mean_length * 2]

print("Anomalies detected from 2023-01-18 12:00:00 to 2023-01-18 13:00:00:")
if anomalies:
    for prefix in anomalies:
        print(f"Prefix: {prefix}, AS Path Length: {as_path_lengths[prefix]}")
else:
    print("No anomalies detected.")
```
## Packet analysis
Given a n3.pcap file containing network traffic data, create a Python script using Scapy to process the PCAP. The script should extract the source IP, destination IP, source port, destination port, and the raw payload data for each packet in the PCAP. Impletent try-except blocks for errors if expected layers IP, TCP/UDP, Raw. Store this data in a pandas DataFrame and display it.

```python
import pandas as pd
from scapy.all import *

# Specify the PCAP file path
pcap_file = 'path/to/traffic.pcap'

try:
    packets = rdpcap(pcap_file)  # Read the PCAP file
    print(f"Total packets in the capture: {len(packets)}\n")

    # Create a list to store packet data
    packet_data = []

    for packet in packets:
        src_ip, dst_ip, src_port, dst_port, raw_data = '', '', '', '', ''
        
        if IP in packet:
            print("IP found")
            # Extract IP information
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst

        if TCP in packet:
            print("TCP found")
            # Extract TCP information
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport

        if Raw in packet:
            print("Raw found")
            # Extract and append raw data (payload)
            raw_data = packet[Raw].load
        packet_data.append([src_ip, dst_ip, src_port, dst_port, raw_data])
    
    # Create a DataFrame from the packet data
    df = pd.DataFrame(packet_data, columns=['Source IP', 'Destination IP', 'Source Port', 'Destination Port', 'Raw Data'])
    
    # Display the DataFrame
    display(df)

except Exception as e:
    print(f"An error occurred: {str(e)}")
```
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Timestamp</th>
      <th>Source MAC</th>
      <th>Destination MAC</th>
      <th>Source IP</th>
      <th>Destination IP</th>
      <th>Source Port</th>
      <th>Destination Port</th>
      <th>Protocol</th>
      <th>Packet Type</th>
      <th>Length</th>
      <th>Raw Data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1615905754.602072</td>
      <td>52:54:00:e2:36:87</td>
      <td>40:de:ad:d9:ed:d9</td>
      <td>172.16.12.2</td>
      <td>10.200.11.70</td>
      <td>2152</td>
      <td>2152</td>
      <td>17</td>
      <td>&lt;class 'scapy.layers.l2.Ether'&gt;</td>
      <td>936</td>
      <td>b'4\xff\x03v@\x02\x01%\x00\x00\x00\x85\x01\x10...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1615905754.603009</td>
      <td>52:54:00:e2:36:87</td>
      <td>40:de:ad:d9:ed:d9</td>
      <td>172.16.12.2</td>
      <td>10.200.11.70</td>
      <td>2152</td>
      <td>2152</td>
      <td>17</td>
      <td>&lt;class 'scapy.layers.l2.Ether'&gt;</td>
      <td>936</td>
      <td>b'4\xff\x03v@\x02\x01%RT\x00\x85\x01\x10\x05\x...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1615905754.604011</td>
      <td>52:54:00:e2:36:87</td>
      <td>40:de:ad:d9:ed:d9</td>
      <td>172.16.12.2</td>
      <td>10.200.11.70</td>
      <td>2152</td>
      <td>2152</td>
      <td>17</td>
      <td>&lt;class 'scapy.layers.l2.Ether'&gt;</td>
      <td>936</td>
      <td>b'4\xff\x03v@\x02\x01%RT\x00\x85\x01\x10\x05\x...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1615905754.605010</td>
      <td>52:54:00:e2:36:87</td>
      <td>40:de:ad:d9:ed:d9</td>
      <td>172.16.12.2</td>
      <td>10.200.11.70</td>
      <td>2152</td>
      <td>2152</td>
      <td>17</td>
      <td>&lt;class 'scapy.layers.l2.Ether'&gt;</td>
      <td>936</td>
      <td>b'4\xff\x03v@\x02\x01%\x00\x00\x00\x85\x01\x10...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1615905754.606004</td>
      <td>52:54:00:e2:36:87</td>
      <td>40:de:ad:d9:ed:d9</td>
      <td>172.16.12.2</td>
      <td>10.200.11.70</td>
      <td>2152</td>
      <td>2152</td>
      <td>17</td>
      <td>&lt;class 'scapy.layers.l2.Ether'&gt;</td>
      <td>936</td>
      <td>b'4\xff\x03v@\x02\x01%\x00\x00\x00\x85\x01\x10...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>87</th>
      <td>1615905754.653013</td>
      <td>52:54:00:e2:36:87</td>
      <td>40:de:ad:d9:ed:d9</td>
      <td>172.16.12.2</td>
      <td>10.200.11.70</td>
      <td>2152</td>
      <td>2152</td>
      <td>17</td>
      <td>&lt;class 'scapy.layers.l2.Ether'&gt;</td>
      <td>936</td>
      <td>b'4\xff\x03v@\x02\x01%\x07\x17\x00\x85\x01\x10...</td>
    </tr>
    <tr>
      <th>88</th>
      <td>1615905754.653530</td>
      <td>40:de:ad:d9:ed:d9</td>
      <td>52:54:00:e2:36:87</td>
      <td>10.200.11.70</td>
      <td>172.16.12.2</td>
      <td>61458</td>
      <td>2152</td>
      <td>17</td>
      <td>&lt;class 'scapy.layers.l2.Ether'&gt;</td>
      <td>936</td>
      <td>b'4\xff\x03v\x00\x00\x00\x01\x00\x00\x00\x85\x...</td>
    </tr>
    <tr>
      <th>89</th>
      <td>1615905754.654010</td>
      <td>52:54:00:e2:36:87</td>
      <td>40:de:ad:d9:ed:d9</td>
      <td>172.16.12.2</td>
      <td>10.200.11.70</td>
      <td>2152</td>
      <td>2152</td>
      <td>17</td>
      <td>&lt;class 'scapy.layers.l2.Ether'&gt;</td>
      <td>936</td>
      <td>b'4\xff\x03v@\x02\x01%\x00\x00\x00\x85\x01\x10...</td>
    </tr>
    <tr>
      <th>90</th>
      <td>1615905754.654535</td>
      <td>40:de:ad:d9:ed:d9</td>
      <td>52:54:00:e2:36:87</td>
      <td>10.200.11.70</td>
      <td>172.16.12.2</td>
      <td>61458</td>
      <td>2152</td>
      <td>17</td>
      <td>&lt;class 'scapy.layers.l2.Ether'&gt;</td>
      <td>936</td>
      <td>b'4\xff\x03v\x00\x00\x00\x01\x00\x00\x00\x85\x...</td>
    </tr>
    <tr>
      <th>91</th>
      <td>1615905754.655008</td>
      <td>52:54:00:e2:36:87</td>
      <td>40:de:ad:d9:ed:d9</td>
      <td>172.16.12.2</td>
      <td>10.200.11.70</td>
      <td>2152</td>
      <td>2152</td>
      <td>17</td>
      <td>&lt;class 'scapy.layers.l2.Ether'&gt;</td>
      <td>936</td>
      <td>b'4\xff\x03v@\x02\x01%\x00\x00\x00\x85\x01\x10...</td>
    </tr>
  </tbody>
</table>
<p>92 rows × 11 columns</p>
</div>

## Performance analysis
Generate Python code to calculate 5G network performance KPIs: Total Network Capacity, Capacity per Area, Capacity per Point, Cost per Capacity, Cost per Area, and Surplus Area. Load data from 'data.csv'. Use keywords: 'capacity', 'cost', 'area', 'numpoints' to identify relevant columns.

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("data.csv")
# Identifying relevant columns using keywords
capacity_columns = [col for col in df.columns if 'capacity' in col.lower()]
cost_columns = [col for col in df.columns if 'cost' in col.lower()]
area_columns = [col for col in df.columns if 'area' in col.lower()]
points_columns = [col for col in df.columns if 'numpoints' in col.lower()]

# Calculate capacity related KPIs using specific columns
df['Total.capacity'] = df['Spectrum.capacity'] + df['Small.cells.capacity']
df['Capacity.per.area'] = df['Total.capacity'] / df['Shape_Area_km2']
df['Capacity.per.point'] = df['Total.capacity'] / df['NUMPOINTS']

# Calculate cost related KPIs using specific columns
df['Cost.per.capacity'] = df['Cost'] / df['Total.capacity']
df['Cost.per.area'] = df['Cost.per.km2'] * df['Shape_Area_km2']

# Calculate surplus related KPIs using identified columns
df['Surplus.per.area'] = df['Capacity.surplus'] / df['Shape_Area_km2']
```
```plaintext
       Total.capacity  Capacity.per.area  Capacity.per.point  \
0           644.68800          40.546415           107.44800   
1           150.56640           9.469585            25.09440   
2            22.76976           1.432060             3.79496   
3           644.68800          40.546415           107.44800   
4           150.56640           9.469585            25.09440   
...               ...                ...                 ...   
36292         0.00000           0.000000             0.00000   
36293       185.49000         206.100000            46.37250   
36294         0.00000           0.000000             0.00000   
36295       185.49000         206.100000            46.37250   
36296         0.00000           0.000000             0.00000   

       Cost.per.capacity  Cost.per.area  Surplus.per.area  
0            2018.654023   1.301402e+06        571.743833  
1            8643.376112   1.301402e+06       1065.865433  
2           18589.596096   4.232806e+05       -621.918240  
3            1362.087372   8.781214e+05        548.974073  
4            5832.120470   8.781214e+05       1043.095673  
...                  ...            ...               ...  
36292                NaN   0.000000e+00      -1208.161800  
36293         521.462555   9.672609e+04     -16445.088000  
36294                NaN   0.000000e+00     -16630.578000  
36295         521.462555   9.672609e+04      -5021.076000  
36296                NaN   0.000000e+00      -5206.566000  
```