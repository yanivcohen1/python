import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates # For formatting dates on the x-axis

# --- Configuration ---
csv_filename = '/system_monitor_detailed.csv'

# --- Main plotting function ---
def plot_csv_data(filename):
    """
    Reads system monitor data from a CSV file and generates a plot.

    Args:
        filename (str): The path to the CSV file.
    """
    try:
        # Read the CSV file into a pandas DataFrame
        # Important: Parse the 'timestamp' column as datetime objects
        df = pd.read_csv(filename, parse_dates=['timestamp'])
        print(f"Successfully loaded data from '{filename}'.")
        print(f"Data contains {len(df)} rows.")

        if df.empty:
            print("The CSV file is empty. No data to plot.")
            return

        # --- Setup Plotting ---
        fig, ax1 = plt.subplots(figsize=(14, 7)) # Make plot wider

        # Configure primary y-axis (for percentages)
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Usage (%)", color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        ax1.set_ylim(0, 105) # Set Y limit slightly above 100%
        # Plot CPU and System Memory percentages against the primary axis
        line_cpu = ax1.plot(df['timestamp'], df['cpu_percent'], 'b-', label='CPU Usage (%)', alpha=0.8, marker='.')
        line_sys_mem = ax1.plot(df['timestamp'], df['system_memory_percent'], 'g-', label='Memory Usage (%)', alpha=0.8, marker='.')
        ax1.legend(loc='upper left')
        ax1.grid(True, axis='y', linestyle='--', alpha=0.6) # Grid lines for primary axis

        # Configure secondary y-axis (for script memory in MB)
        ax2 = ax1.twinx() # instantiate a second axes that shares the same x-axis
        ax2.set_ylabel(f"Process Memory RSS (MB)", color='tab:red')
        ax2.tick_params(axis='y', labelcolor='tab:red')
        # Plot Script Memory against the secondary axis
        line_script_mem = ax2.plot(df['timestamp'], df['script_memory_rss_mb'], 'r-', label='Script Memory RSS (MB)', alpha=0.8, marker='.')
        ax2.legend(loc='upper right')
        # Set bottom limit for secondary axis, let top autoscale
        ax2.set_ylim(bottom=0)


        # --- Formatting ---
        fig.suptitle(f'System Resource Usage for process {df['script_pid'][0]} from Log File', fontsize=16)

        # Improve x-axis date formatting
        locator = mdates.AutoDateLocator(minticks=5, maxticks=10) # Auto-choose tick locations
        formatter = mdates.ConciseDateFormatter(locator) # Auto-choose format based on scale
        ax1.xaxis.set_major_locator(locator)
        ax1.xaxis.set_major_formatter(formatter)
        fig.autofmt_xdate() # Auto format dates to prevent overlap

        ax2.autoscale(axis='y', enable=True)
        ax1.autoscale(axis='y', enable=True)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to prevent title overlap
        # plt.title(f"system resource for process {df['script_pid'][0]}", fontsize=14)
        plt.show() # Display the plot

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{filename}' is empty or corrupted.")
    except KeyError as e:
        print(f"Error: Missing expected column in CSV file: {e}. Was the file generated correctly?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Run the plotting function ---
if __name__ == "__main__":
    current_directory = os.path.dirname(__file__)
    plot_csv_data(current_directory + csv_filename)
