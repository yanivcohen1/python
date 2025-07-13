import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Define the ODE function
def f(t, y):
    return -y  # return dy/dt = -y


# Initial conditions
y0 = 1

# Time interval
t_span = (0, 5)

# Solve the ODE
sol = solve_ivp(f, t_span, [y0])

# Extract the solution
t = sol.t
y = sol.y[0]  # Extract the first component (y)

# Print the solution at some points
print("Solution (t, y):")
for i in range(0, len(t), 5):
    print(f"({t[i]:.4f}, {y[i]:.4f})")

plt.plot(t, y)
plt.xlabel("t")
plt.ylabel("y")
plt.title("Solution of dy/dt = -y")
plt.grid(True)
plt.show()
