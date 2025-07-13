import numpy as np
import matplotlib.pyplot as plt

# Define grid
x = np.linspace(-1.5, 1.5, 400)
y = np.linspace(-1.5, 1.5, 400)
X, Y = np.meshgrid(x, y)

# Define region: inside unit circle and above y = x
region = (X**2 + Y**2 < 1) & (Y > X)

# Convert boolean to integer (1 for True, 0 for False)
region_int = region.astype(int)

plt.figure(figsize=(6, 6))
plt.contour(X, Y, region_int, colors=["blue"])
plt.xlabel("x")
plt.ylabel("y")
plt.title("Region: $x^2 + y^2 < 1$ and $y > x$")
plt.axis("equal")
plt.grid(True)
plt.show()

# Automatically calculate contour levels based on region_int data
min_val = region_int.min()   # will be 0
max_val = region_int.max()   # will be 1

# Compute a threshold: for a binary array 0 and 1, the mid-value is 0.5
threshold = (min_val + max_val) / 2

# Use the threshold to calculate the levels for contouring:
# The lower level is the threshold, and the upper is threshold + max_val (0.5 + 1 = 1.5 in this case)
lower_level = threshold           # 0.5
upper_level = max_val + threshold   # 1 + 0.5 = 1.5

levels = [lower_level, upper_level]
print("Calculated levels:", levels)

# Plot only the region where condition is True (value = 1)
plt.figure(figsize=(6, 6))
plt.contourf(X, Y, region_int, levels=levels, colors=["blue"])
plt.xlabel("x")
plt.ylabel("y")
plt.title("Region: $x^2 + y^2 < 1$ and $y > x$")
plt.axis("equal")
plt.grid(True)
plt.show()


