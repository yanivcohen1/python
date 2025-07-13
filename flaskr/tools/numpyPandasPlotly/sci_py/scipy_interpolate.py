import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange

# Given data points
x = np.array([0, 1, 2])
y = np.array([1, 3, 2])

# Compute the Lagrange polynomial
poly = lagrange(x, y)

# Convert polynomial to a more convenient form
coefficients = np.poly1d(poly.coefficients)
print(f"The interpolating polynomial is:\n{coefficients}")

# Generate a range of x values for plotting the polynomial
x_vals = np.linspace(min(x-1), max(x+1), 100)
y_vals = coefficients(x_vals)
f = lambda x : -1.5 * x**2 + 3.5 * x + 1

# Plot the polynomial
plt.plot(x_vals, y_vals, label='Polynomial Interpolation')
plt.plot(x_vals, f(x_vals), ".", label='Poly find: -1.5x^2 + 3.5x + 1')
# Plot the original data points
plt.plot(x, y, 'ro', label='Data Points')

# Add labels and legend
plt.xlabel('x')
plt.ylabel('y')
plt.title('Polynomial Interpolation')
plt.legend()

# Show the plot
plt.show()
