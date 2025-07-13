import numpy as np
import matplotlib.pyplot as plt

# entral difference method for drive x^2

# Define the function
def f(x):
    return x**3

# Define the central difference method
def central_difference(f, x, h):
    return (f(x + h) - f(x)) / (h)
    # Define the central difference method
    # return (f(x + h) - f(x - h)) / (2 * h)

# Define the range for x and the step size h
x = np.linspace(-10, 10, 100)
h = 0.1

# Calculate the derivative using the central difference method
derivatives = [central_difference(f, xi, h) for xi in x]

y_exact = 3*x**2

# Plot the function and its derivative
plt.figure(figsize=(10, 5))

# Plot the original function
plt.subplot(1, 2, 1)
plt.plot(x, f(x), label='f(x) = x^3')
plt.title('Function x^3')
plt.grid(True)
plt.legend()

# Plot the derivative
plt.subplot(1, 2, 2)
plt.plot(x, derivatives, label="f'(x) Approximation", color='orange')
plt.plot(x, y_exact, '--', label="The exact solution is y = 3x^2")
plt.title('Derivative is 3x^2')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
