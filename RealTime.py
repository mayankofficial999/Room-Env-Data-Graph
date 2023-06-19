from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

# Firebase credentials and initialization
cred = credentials.Certificate('./service_secrets.json')
rtdbUrl = 'YOUR_RTDB_URL'
firebase_admin.initialize_app(cred, {
    'databaseURL': rtdbUrl
})

# Firebase RTDB path
rtdb_path = '/Stats/Data'

# Initialize lists for storing data
timestamps = []
temperatures = []
humidities = []


# Extract the latest data
current_time = datetime.now()
x = input('Enter prev hours to include: ')
if len(x) == 0:
    x = 1
else:
    x = int(x)
x_hours_ago = current_time - timedelta(hours=x)

# Create a figure and axis
fig, ax = plt.subplots()
# Set the figure title
fig.canvas.set_window_title('Room Temperature & Humidity')

# Create empty lines for the plot
temperature_line, = ax.plot([], [], label='Temperature')
humidity_line, = ax.plot([], [], label='Humidity')

# Function to initialize the plot
def init_plot():
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.legend()
    plt.xticks(rotation=45)

# Function to format time in 12-hour format
def format_time(ts):
    dt = datetime.fromtimestamp(ts)
    return dt.strftime('%I:%M:%S %p')

# Function to update the plot
def update_plot(frame):
    global timestamps, temperatures, humidities

    # Fetch data from Firebase
    ref = db.reference(rtdb_path)
    data = ref.get()

    if data is None:
        return

    # Clear the lists
    timestamps.clear()
    temperatures.clear()
    humidities.clear()

    for timestamp, values in data.items():
        timestamp = int(timestamp)
        temperature = values.get('Temperature')
        humidity = values.get('Humidity')

        if temperature is None or humidity is None:
            continue

        timestamps.append(timestamp)
        temperatures.append(temperature)
        humidities.append(humidity)

    # Trim the lists to the last 3 hours
    while timestamps and datetime.fromtimestamp(timestamps[0]) < x_hours_ago:
        timestamps.pop(0)
        temperatures.pop(0)
        humidities.pop(0)

    # Update the plot data
    temperature_line.set_data(timestamps, temperatures)
    humidity_line.set_data(timestamps, humidities)

    # Adjust the plot limits if needed
    ax.relim()
    ax.autoscale_view()

    # Format the x-axis ticks as time in 12-hour format
    ax.set_xticklabels([format_time(ts) for ts in ax.get_xticks()])

# Set up the animation
ani = FuncAnimation(fig, update_plot, init_func=init_plot, interval=5000)

# Display the plot
plt.show()