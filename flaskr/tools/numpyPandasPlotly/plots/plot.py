import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# https://matplotlib.org/stable/gallery/
# https://www.youtube.com/watch?v=xcONCZR6bMo&t=263s
# https://github.com/derekbanas/Python4Finance/blob/main/Numpy_Pandas.ipynb

print(pd.to_datetime(['2018-10-26 12:00 -0530', '2018-10-26 12:00 -0500'],
                utc=True)[0]) # print in utc: 2018-10-26 17:30:00+00:00

# -------- panda for table data menipulation -------------------
csv = {
  "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
  "Sales": [1000, 1200, 1500, 1800, 2000, 2200],
  "Profit": [200, 300, 400, 500, 600, 700],
  'time': [1, 2, 3],
}

table = pd.DataFrame(csv, columns=['Month', 'Sales', "Profit"])# option to fillter
# table = pd.read_csv('data.csv')

# Panda print 2 first rows
# use a list of indexes:
print(table.loc[[0, 1]])
#    Month  Sales  Profit
# 0   Jan   1000     200
# 1   Feb   1200     300

# create a figure and an Axes
fig, ax = plt.subplots()

# plot a line plot of the Sales column with points
table.plot.line(x="Month", y=["Sales", "Profit"], ax=ax, marker=".", title="plot for panda data") # , markersize=10

plt.ylabel('Money')
# show the figure
plt.grid(True)
plt.show()

# ------ nupmy for math 2d and 3d ----------------------

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

# Plot the real part
plt.plot(t, psi_real, label='Real part')
plt.grid(True)
# plt.xlabel('Time')
# plt.ylabel('Wave function')
# plt.title('Real part of the wave function at x=0')
# plt.legend()
# plt.show()

# Plot the imaginary part
plt.plot(t, psi_imag, label='Imaginary part', marker='.')
plt.plot(t, np.abs(psi), label='|psi|')
plt.plot(t, psi**2, '--', label='psi^2')
plt.plot(t, np.arctan(psi_real/psi_imag)/(np.pi), label='psi angle')
plt.xlabel('Time')
plt.ylabel('Wave function')
plt.axvline(2, color="k", ls="--", label="start")
plt.axvline(4, color="k", ls="-.", label="end")
plt.text(2, 0.5, 'start limit', ha='left', va='bottom', color="green")
plt.annotate(f'P={2.0:.2f}', xy=(2, 0.2), xytext=(0, 10), # xytext is the text offset point [2, (0.2 + 10)]
                textcoords='offset points', ha='center', color='red')
plt.title('plot for numpy data')
plt.legend()
plt.grid(True)
plt.show()


# print in subPlot
fig = plt.figure(figsize=(10, 5))
ax1 = plt.subplot(1, 2, 1) # in y are 1 plot, in x are 2 plots, 1 plot
ax1.plot(t, psi_real, label="Real part")
ax1.set_xlabel("Time")
ax1.set_ylabel("Wave function")
ax1.set_title('Real Wave function')
ax1.legend()
ax1.grid(True)
ax2 = plt.subplot(1, 2, 2) # in y are 1 plot, in x are 2 plots, 2 plot
ax2.plot(t, psi_imag, "r.-", label="Imaginary part")
ax2.plot(t, psi_real, "--", label="Real part")
ax2.set_xlabel("Time")
ax2.set_ylabel("Wave function")
ax2.set_title('Mix Wave function')
ax2.legend()
ax2.grid(True)
plt.show()


# print subplot [2, 2]
y = np.real(psi)
x = t
fig = plt.figure(figsize=(10, 5))
axs = fig.subplots(2, 2)
axs[0, 0].plot(x, y)
axs[0, 0].set_title('Axis [0, 0]')
axs[0, 1].plot(x, y, 'tab:orange')
axs[0, 1].set_title('Axis [0, 1]')
axs[1, 0].plot(x, -y, 'tab:green')
axs[1, 0].set_title('Axis [1, 0]')
axs[1, 1].plot(x, -y, 'tab:red')
axs[1, 1].set_title('Axis [1, 1]')

for ax in axs.flat:
    ax.set(xlabel='x-label', ylabel='y-label')
    ax.grid(True)

axs[1, 1].set_xlabel("Time")
axs[1, 1].set_ylabel("Wave function")

fig.suptitle("common label latex syntax $\psi=0$")
fig.tight_layout()
fig.show()
plt.show()
