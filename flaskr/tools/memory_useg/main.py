import psutil
import time
import datetime
import csv
import os
import matplotlib.pyplot as plt
from collections import deque

# --- Configuration ---
log_file = '/system_monitor_detailed.csv'
log_interval_seconds = 5  # Check every 5 seconds for faster plot updates
plot_update_interval_seconds = 5 # How often to redraw the plot
max_plot_points = 100  # Keep the last 100 data points for the plot

# --- Data Storage for Plotting ---
timestamps = deque(maxlen=max_plot_points)
cpu_usage_hist = deque(maxlen=max_plot_points)
sys_mem_usage_hist = deque(maxlen=max_plot_points)
script_mem_usage_hist = deque(maxlen=max_plot_points) # In MB

# --- Get Current Script's PID ---
script_pid = os.getpid()
try:
    script_process = psutil.Process(script_pid)
    print(f"Monitoring script process with PID: {script_pid}")
except psutil.NoSuchProcess:
    print(f"Error: Could not find script process with PID: {script_pid}")
    script_process = None # Set to None if process not found

# --- Setup Logging ---
current_directory = os.path.dirname(__file__)
log_file = current_directory + log_file
file_exists = os.path.isfile(log_file)
csvfile = open(log_file, 'a', newline='', buffering=1) # Use line buffering
fieldnames = [
    'timestamp', 'cpu_percent', 'system_memory_percent', 'system_memory_used_mb',
    'script_pid', 'script_memory_rss_mb'
]
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
if not file_exists:
    writer.writeheader() # File doesn't exist yet, write a header

# --- Setup Plotting ---
plt.ion() # Turn on interactive mode
fig, ax1 = plt.subplots(figsize=(12, 6))

# Configure primary y-axis (for percentages)
ax1.set_xlabel("Time")
ax1.set_ylabel("Usage (%)", color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.set_ylim(0, 105) # Set Y limit slightly above 100%
line_cpu, = ax1.plot([], [], 'b-', label='CPU Usage (%)', marker='.')
line_sys_mem, = ax1.plot([], [], 'g-', label='Memory Usage (%)', marker='.')
ax1.legend(loc='upper left')
ax1.grid(True)

# Configure secondary y-axis (for script memory in MB)
ax2 = ax1.twinx() # instantiate a second axes that shares the same x-axis
ax2.set_ylabel(f"Memory RSS (MB)", color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')
ax2.set_ylim(bottom=0) # Start y-axis at 0
line_script_mem, = ax2.plot([], [], 'r-', label='Script Memory RSS (MB)', marker='.')
ax2.legend(loc='upper right')

fig.suptitle(f'System Resource Monitor for process: {script_process.name()}({script_pid})')
fig.autofmt_xdate() # Auto format dates on x-axis

last_plot_time = time.time()

# --- Monitoring Loop ---
print(f"Starting monitoring... Logging to '{log_file}' every {log_interval_seconds}s.")
print("Press Ctrl+C to stop.")
cpu_usage = 0 # Default to 0 before first read
try:
    while True:
        current_time = time.time()
        now = datetime.datetime.now()
        timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")

        # --- Get System Metrics ---
        memory_info = script_process.memory_info().vms if script_process else None # virtual memory size (vms)
        memory_info_all = psutil.virtual_memory().used # Total used memory in bytes
        system_memory_usage_percent = memory_info / memory_info_all
        system_memory_used_mb = memory_info / (1024 * 1024)

        # --- Get Specific Script Metrics ---
        script_memory_rss_mb = 0 # Default to 0
        if script_process:
            try:
                cpu_usage = script_process.cpu_percent(interval=0.1) # psutil.cpu_percent(interval=0.5) # Shorter interval for responsiveness
                # Get memory info for the specific script process
                script_mem_info = script_process.memory_info()
                # RSS (Resident Set Size) is often a good measure of actual physical memory used
                script_memory_rss_mb = script_mem_info.rss / (1024 * 1024)
            except psutil.NoSuchProcess:
                print(f"Warning: Script process {script_pid} not found. Stopping its monitoring.")
                script_process = None # Stop trying to monitor it
            except Exception as e:
                print(f"Warning: Could not get memory info for PID {script_pid}: {e}")

        # --- Log Data ---
        log_data = {
            'timestamp': timestamp_str,
            'cpu_percent': cpu_usage,
            'system_memory_percent': system_memory_usage_percent,
            'system_memory_used_mb': round(system_memory_used_mb, 2),
            'script_pid': f"{script_process.name()}({script_pid})" if script_process else 'N/A',
            'script_memory_rss_mb': round(script_memory_rss_mb, 2)
        }
        writer.writerow(log_data)
        # csvfile.flush() # Flushing frequently can impact performance, rely on buffering=1

        print(f"{timestamp_str} - Logged: CPU {cpu_usage:.2f}%, Mem {system_memory_usage_percent:.2f}%, Mem {script_memory_rss_mb:.2f} MB")

        # --- Update Plot Data ---
        timestamps.append(now) # Use datetime objects for plotting
        cpu_usage_hist.append(cpu_usage)
        sys_mem_usage_hist.append(system_memory_usage_percent)
        script_mem_usage_hist.append(script_memory_rss_mb)

        # --- Redraw Plot periodically ---
        if current_time - last_plot_time >= plot_update_interval_seconds:
            last_plot_time = current_time

            # Update line data
            line_cpu.set_data(list(timestamps), list(cpu_usage_hist))
            line_sys_mem.set_data(list(timestamps), list(sys_mem_usage_hist))
            line_script_mem.set_data(list(timestamps), list(script_mem_usage_hist))

            # Adjust plot limits
            ax1.relim()
            ax1.autoscale_view()
            ax2.relim()
            ax2.autoscale_view() # Autoscale secondary axis based on its data

            # Keep primary y-axis fixed from 0-105%
            ax1.set_ylim(0, 105)
            # Ensure secondary y-axis starts at 0
            ax2_ylim = ax2.get_ylim()
            # ax2.set_ylim(0, ax2_ylim[1] * 1.1) # Add 10% padding to top
            # ax2.set_ylim(bottom=0)
            ax2.autoscale(axis='y', enable=True)
            ax1.autoscale(axis='y', enable=True)


            # Redraw the figure
            fig.canvas.draw()
            fig.canvas.flush_events()
            print("Plot updated.")


        # --- Wait for the next interval ---
        # Calculate sleep time needed to maintain the interval
        elapsed_time = time.time() - current_time
        sleep_time = max(0, log_interval_seconds - elapsed_time)
        # time.sleep(sleep_time)
        plt.pause(sleep_time)

except KeyboardInterrupt:
    print("Monitoring stopped by user.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # --- Cleanup ---
    print("Closing log file and plot.")
    if csvfile:
        csvfile.close()
    plt.ioff() # Turn off interactive mode
    plt.close(fig) # Close the plot window
    print("Cleanup complete.")

