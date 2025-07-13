# https://plotly.com/python/shapes/
import plotly.graph_objects as go

# Create a scatter plot triangular
fig = go.Figure(go.Scatter(x=[0, 1, 2, 0], y=[0, 2, 0, 0], fill="toself"))

# Add a rectangle
fig.add_shape(type="rect", fillcolor='turquoise',
              x0=1, y0=1, x1=2, y1=3, label=dict(text="Text in rectangle"))

# Add a circle
fig.add_shape(type="circle",
    xref="x", yref="y",
    fillcolor="PaleTurquoise",
    x0=3, y0=3, x1=4, y1=4,
    line_color="LightSeaGreen",
)

# Add a line
fig.add_shape(type="line", xref="x", yref="y",
            x0=3, y0=0.5, x1=5, y1=0.8, line_width=3)

# add Custom shape
fig.add_shape(type="path",
              path=" M 2,2 L 2,3 L 4,1 Z",
              fillcolor="LightPink",
              line_color="Crimson")

# Show the figure
fig.show()
