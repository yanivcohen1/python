from matplotlib.axes import Axes
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# https://matplotlib.org/stable/gallery/
# https://www.youtube.com/watch?v=xcONCZR6bMo&t=263s
# https://github.com/derekbanas/Python4Finance/blob/main/Numpy_Pandas.ipynb

# Define the parameters
a = 1 # length scale
hbar = 1 # reduced Planck constant
m = 1 # mass

# Define the time range
t = np.linspace(0, 10, 100)

# Define the wave function at x=0
psi = 1/np.sqrt(np.pi*a**2)*np.exp(-1j*hbar/a**2*t)

# Extract the real and imaginary parts
psi_real = np.real(psi)
psi_imag = np.imag(psi)


# print subplot [2, 2]
y = np.real(psi)
x = t
fig = plt.figure(figsize=(10, 5))
axs = fig.subplots(2, 2)# 2 in x and 2 in y
ax4: Axes = axs[1, 1]
# ax1: Axes, ax2: Axes, ax3: Axes, ax4: Axes = axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]
axs[0, 0].plot(x, y)
axs[0, 0].set_title('Axis [0, 0]')
axs[0, 1].plot(x, y, 'tab:orange')
axs[0, 1].set_title('Axis [0, 1]')
axs[1, 0].plot(x, -y, 'tab:green')
axs[1, 0].set_title('Axis [1, 0]')
ax4.plot(x, -y, label="Real part", marker='.')
ax4.plot(x, y, "--",label="Imaginary part")
ax4.set_title('Axis [1, 1]')

for ax in axs.flat:
    ax.set(xlabel='x-label', ylabel='y-label')
    ax.grid(True)

ax4.set_xlabel("Time")
ax4.set_ylabel("Wave function")
ax4.legend()

fig.suptitle("common label")
fig.tight_layout()
fig.show()
plt.show()


# print in subPlot
plt.figure(figsize=(10, 5))
# print in plot 1 from subPlot
ax1 = plt.subplot(1, 2, 1) # in y are 1 plot, in x are 2 plots, 1 plot
ax1.plot(t, psi_real, label="Real part")
ax1.set_xlabel("Time")
ax1.set_ylabel("Wave function")
ax1.set_title('Real Wave function')
ax1.grid()
ax1.legend()
# print in plot 2 from subPlot
ax2 = plt.subplot(1, 2, 2) # in y are 1 plot, in x are 2 plots, 2 plot
ax2.plot(t, psi_imag, "r.-", label="Imaginary part")
ax2.plot(t, psi_real, "--", label="Real part")
ax2.set_xlabel("Time")
ax2.set_ylabel("Wave function")
ax2.set_title('Mix Wave function')
ax2.legend()
ax2.grid()
plt.show()


# print in plot 1 of 1 from subPlot
ax1 = plt.subplot(1, 1, 1) # in y are 1 plot, in x are 1 plots, 1 plot
ax1.plot(t, -psi_real, label="Real part", marker=".")
ax1.set_xlabel("Time")
ax1.set_ylabel("Wave function")
ax1.set_title('Real Wave function')
ax1.legend()
ax1.grid(True)
plt.show()
