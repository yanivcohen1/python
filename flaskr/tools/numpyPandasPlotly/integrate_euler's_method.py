import numpy as np
import matplotlib.pyplot as plt

# Euler's Method for integrate dy/dx = x + y; y0 = 1

# Define the function that represents the derivative dy/dx
def derivative(x, y):
    return x + y

# Initial conditions
x0 = 0
y0 = 1
h = 0.01  # Step size
x_end = 2

# Create an array of x values from x0 to x_end with a step size h
x_values = np.arange(x0, x_end + h, h)

# Initialize an array to store the y values
y_values = [y0]

# Apply Euler's method
for i in range(1, len(x_values)):
    x = x_values[i-1]
    y = y_values[-1]
    y_next = y + h * derivative(x, y) # y(x+dx) = y(x) + dy(x); dy(x) = dx * y'(x)
    y_values.append(y_next)

y_exact =  2 * np.exp(x_values) - x_values - 1  # Exact solution

# Plot the differential equation and its solution
plt.figure(figsize=(12, 5))

# Plot the differential equation
plt.subplot(1, 2, 1)
plt.plot(x_values, derivative(x_values, y0), 'r-', label="dy/dx")
plt.title("Differential Equation dy/dx = x + y; y0 = 1")
plt.xlabel('x')
plt.ylabel('dy/dx')
plt.legend()
plt.grid(True)

# Plot Euler's method solution
plt.subplot(1, 2, 2)
plt.plot(x_values, y_values, 'b-', label="Euler's Method Approximation")
plt.plot(x_values, y_exact, 'r--', label="The exact solution is y = 2e^x - x - 1")
plt.title("Euler's Method The exact solution is y = 2e^x - x - 1")
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
