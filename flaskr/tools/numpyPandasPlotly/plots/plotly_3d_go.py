# https://plotly.com/python/
# https://www.geeksforgeeks.org/python-plotly-tutorial/
import plotly.graph_objects as go
import numpy as np

# Data to be plotted
# x = np.outer(np.linspace(-2, 2, 30), np.ones(30))
# y = x.copy().T
# z = np.cos(x ** 2 + y ** 2)

x = np.linspace(-2, 2, 50)
y = np.linspace(-2, 2, 40)
y1 = y[:, np.newaxis]
z = np.sin(x) * np.cos(y1)
z = np.cos(x ** 2 + y1 ** 2)
# array([0, 1, 2])
# x[:, newaxis]
# array([[0], [1], [2]])

X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
x, y = np.meshgrid(X, Y)
R = np.sqrt(x**2 + y**2)
z = np.sin(R)

# plotting the figure 3D
fig = go.Figure(data=[go.Surface(x=x, y=y, z=z)])

fig.update_layout(title="Plotted 3D")

fig.show()


# Create the heatmap
fig = go.Figure(data=go.Heatmap(
    z=z,
    x=X,
    y=Y
))

# Show the figure
fig.show()
