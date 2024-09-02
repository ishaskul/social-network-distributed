import matplotlib.pyplot as plt

# Initialize lists to hold time and CPU usage data
timestamps = []
cpu_usages = []

# Read the `cpu_usage.txt` file
with open('./socialNetwork/cpu_usage.txt', 'r') as file:
    for line in file:
        # Only process lines that contain CPU usage data
        if 'Average:' not in line and 'CPU' not in line:
            columns = line.split()
            if len(columns) > 3:
                timestamps.append(columns[0])  # Time
                cpu_usages.append(100 - float(columns[7]))  # Idle is column 7, so 100 - idle = usage

# Plot the CPU usage data
plt.plot(timestamps, cpu_usages, label="CPU Usage (%)")
plt.xlabel('Time')
plt.ylabel('CPU Usage (%)')
plt.title('CPU Usage Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()

# Save the plot as an image
plt.savefig('cpu_usage_plot.png')

# Show the plot
plt.show()
