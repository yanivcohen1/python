import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import animation

fig = plt.figure()
ax: Axes3D = fig.add_subplot(111, projection='3d')

def gen(n):
    phi = 0
    while phi < 2 * np.pi:
        yield np.array([np.cos(phi), np.sin(phi), phi])
        phi += 2 * np.pi / n

def update(num, data, line):
    line.set_data(data[:2, :num])
    line.set_3d_properties(data[2, :num])

N = 100
data = np.array(list(gen(N))).T
line, = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1])

# Setting the axes properties
ax.set_xlim3d([-1.0, 1.0])
ax.set_xlabel('X')
ax.set_ylim3d([-1.0, 1.0])
ax.set_ylabel('Y')
ax.set_zlim3d([0.0, 10.0])
ax.set_zlabel('Z')

# Add mouse interaction
def on_mouse(event):
    if event.button == 'up':
        ax.view_init(elev=ax.elev + 10, azim=ax.azim)
    elif event.button == 'down':
        ax.view_init(elev=ax.elev - 10, azim=ax.azim)
    fig.canvas.draw()

fig.canvas.mpl_connect('scroll_event', on_mouse)

ani = animation.FuncAnimation(fig, update, N, fargs=(data, line), interval=10000 / N, blit=False)
plt.title("animation mouse event on scroll")
plt.show()
