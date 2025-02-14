import pandas as pd

# Example timestamps (replace this with your actual data)
timestamps = [
    "12:15:36.064",
    "12:15:42.043",
    "12:15:49.076",
    "12:16:05.064",
    "12:16:05.064",
    "12:16:11.070",
    "12:16:11.071",
    "12:16:18.069",
    "12:16:19.080",
    "12:16:25.074",
    "12:16:28.070",
    "12:16:54.072",
    "12:16:55.050",
    "12:16:56.065",
    "12:16:56.066",
    "12:17:04.069",
    "12:17:06.069",
    "12:17:15.071",
    "12:17:19.073",
    "12:17:21.066",
    "12:17:29.074",
    "12:17:32.077",
    "12:17:43.067",
    "12:17:44.072",
    "12:17:47.074",
    "12:17:56.072",
    "12:17:56.073",
    "12:18:04.073",
    "12:18:12.073",
    "12:18:15.074",
    "12:18:16.056",
    "12:18:31.074",
    "12:18:37.069",
    "12:18:37.070",
    "12:18:38.073",
    "12:18:44.044",
    "12:18:47.050",
    "12:18:53.069"
]

# Convert timestamps to a pandas DataFrame
df = pd.DataFrame({"timestamps": pd.to_datetime(timestamps)})

# Calculate time intervals in seconds
df["time_diff"] = df["timestamps"].diff().dt.total_seconds()

# Calculate the metrics
average_interval = df["time_diff"].mean()
max_interval = df["time_diff"].max()
min_interval = df["time_diff"].min()

# Print the results
print("Average time interval:", average_interval, "seconds")
print("Maximum time interval:", max_interval, "seconds")
print("Minimum time interval:", min_interval, "seconds")
