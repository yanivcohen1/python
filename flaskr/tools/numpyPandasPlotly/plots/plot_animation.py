import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
n = 1000
x = np.linspace(0, 6*np.pi, n)
y = np.sin(x)

# Define the meta data for the movie
# FFMpegWriter = manimation.writers['ffmpeg']
# metadata = dict(title='Movie Test', artist='Matplotlib',
#                 comment='a red circle following a blue sine wave')
# writer = FFMpegWriter(fps=15, metadata=metadata)

# Initialize the movie
fig = plt.figure()

# plot the sine wave line
sine_line, = plt.plot(x, y, 'b')
red_circle, = plt.plot([], [], 'ro', markersize = 10)
plt.xlabel('x')
plt.ylabel('sin(x)')

for i in range(n):
    x0 = x[i]
    y0 = y[i]
    red_circle.set_data([x0], [y0])
    plt.pause(0.01)

plt.show()
