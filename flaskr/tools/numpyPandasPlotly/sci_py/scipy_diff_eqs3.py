import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# solve this eq's
# h'(t) = i(t) + 4h(t) +1
# i'(t) = 2i(t) + h(t) +1

# Define the initial conditions
h0 = 0  # Initial value for h(t)
i0 = 1  # Initial value for i(t)

# Define the time step and total time
dt = 0.01  # Time step
T = 10  # Total time

# Create arrays to store the values of h(t) and i(t)
t_values = np.arange(0, T, dt)
h_values = np.zeros_like(t_values)
i_values = np.zeros_like(t_values)

# Implement Euler's method
for i in range(len(t_values) - 1):
    h_prime = i_values[i] + 4 * h_values[i] + 1
    i_prime = 2 * i_values[i] + h_values[i] + 1
    h_values[i + 1] = h_values[i] + h_prime * dt
    i_values[i + 1] = i_values[i] + i_prime * dt

# Plot the results
plt.figure(figsize=(8, 6))
plt.plot(t_values, h_values,"-", label="Euler h(t)")
plt.plot(t_values, i_values,"--", label="Euler i(t)")
plt.xlabel("Time (t)")
plt.ylabel("Values")
plt.title("Solution of the System of Differential Equations")
plt.legend()
plt.grid(True)
# plt.show()


# Define the system of differential equations
def system(y, t):
    h, i = y # folow the init vals format
    dh_dt = i + 4 * h + 1
    di_dt = 2 * i + h + 1
    return [dh_dt, di_dt] # folow the init vals format

initial_conditions = [h0, i0]
# Solve the system
solution = odeint(system, initial_conditions, t_values)

# Extract h(t) and i(t) from the solution
h_values, i_values = solution[:, 0], solution[:, 1]

# Plot the results
# plt.figure(figsize=(8, 6))
plt.plot(t_values, h_values,"-", label="odeint h(t)")
plt.plot(t_values, i_values,"--", label="odeint i(t)")
plt.xlabel("Time (t)")
plt.ylabel("Values")
plt.title("Solution of the System of Differential Equations")
plt.legend()
plt.grid(True)

plt.show()
