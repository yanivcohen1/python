from tqdm.auto import tqdm
import time

# The code snippet demonstrates how to use the `tqdm` library to create a progress bar in Python.
for i in tqdm(range(10)):
    time.sleep(0.3)  # Simulate some work being done
