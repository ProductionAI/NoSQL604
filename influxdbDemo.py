# $ pip install influxdb_client
import time
from datetime import datetime, timezone
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# --- Configuration ---
INFLUX_URL   = "http://localhost:8086"
INFLUX_TOKEN = "my-super-secret-token"
INFLUX_ORG   = "my-org"
INFLUX_BUCKET = "my-bucket"

# --- Connect ---
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

# --- Write some data points ---
print("Writing data...")
for i in range(5):
    point = (
        Point("cpu_usage")           # measurement name
        .tag("host", "server-01")    # tag (indexed metadata)
        .tag("region", "us-east")
        .field("usage_percent", 40.0 + i * 5)   # field (actual value)
        .field("temperature", 55.0 + i)
        .time(datetime.now(timezone.utc), WritePrecision.NS)
    )
    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
    time.sleep(0.1)

print("Done writing.\n")

# --- Query data back (Flux query language) ---
query = f'''
from(bucket: "{INFLUX_BUCKET}")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "cpu_usage")
  |> filter(fn: (r) => r.host == "server-01")
'''

print("Querying data:")
tables = query_api.query(query, org=INFLUX_ORG)

for table in tables:
    for record in table.records:
        print(f"  [{record.get_time()}]  {record.get_field()} = {record.get_value()}")

# --- Clean up ---
client.close()