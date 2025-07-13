import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class Interactive3DPlot:
    def __init__(self, fig, ax: Axes3D):
        self.fig = fig
        self.ax = ax
        self.cid = fig.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        msg = f"Clicked Position: x={event.xdata:.2f}, y={event.ydata:.2f}"
        print(msg)
        xs = np.random.rand(100)
        ys = np.random.rand(100)
        zs = np.random.rand(100)
        self.ax.clear()
        self.ax.scatter(xs, ys, zs)
        plt.title(msg)

    def plot(self, xs, ys, zs):
        self.scatter = self.ax.scatter(xs, ys, zs)

# Generate random data
xs = np.random.rand(100)
ys = np.random.rand(100)
zs = np.random.rand(100)

# Set up the figure and axis
fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(111, projection='3d')


# Create the interactive plot
interactive_plot = Interactive3DPlot(fig, ax)
interactive_plot.plot(xs, ys, zs)
plt.title("plot with mouse interactions")

plt.show()
