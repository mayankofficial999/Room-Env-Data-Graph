import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date, datetime

# Path to the JSON file
json_file = './data.json'

# Load the data from JSON
with open(json_file) as f:
    data = json.load(f)

timestamps = []
temperatures = []
humidities = []

# Get the current date
current_date = date.today()

# Input the custom date
custom_date = input("Enter the custom date (YYYY-MM-DD): ")


if len(custom_date) != 0:
    datetime.strptime(custom_date, "%Y-%m-%d").date()
else:
    custom_date = current_date

# Extract the data for the custom date from the JSON dictionary
for timestamp, values in data.items():
    # Convert timestamp from epoch seconds to datetime object
    dt = datetime.fromtimestamp(int(timestamp))
    # Check if the date matches the custom date
    if dt.date() == custom_date:
        timestamps.append(dt)
        temperatures.append(values['Temperature'])
        humidities.append(values['Humidity'])

# Create a figure and axis
fig, ax = plt.subplots()

# Plot temperature
ax.plot(timestamps, temperatures, label='Temperature')

# Plot humidity
ax.plot(timestamps, humidities, label='Humidity')

# Format the x-axis as hours
date_format = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()

# Add labels and legend
ax.set_xlabel('Time')
ax.set_ylabel('Value')
ax.legend()

# Display the plot
plt.show()
