import matplotlib.pyplot as plt
import numpy as np

x_range = y_range = np.linspace(0, 2*np.pi, 100)
x, y = np.meshgrid(x_range, y_range)
fx, fy = np.sin(x), np.cos(y)
f_mag = np.sqrt(fx**2 + fy**2)
plt.figure(figsize=(5, 5))
plt.imshow(f_mag, origin="lower", extent=(0, 2*np.pi, 0, 2*np.pi), cmap="gray")
plt.quiver(x[::10, ::10], y[::10, ::10], fx[::10, ::10], fy[::10, ::10], pivot="middle", color="red")
plt.show()
