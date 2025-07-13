from vpython import *

# Create a canvas
scene = canvas(title='Click on Sphere to Move Sphere')

# Initial position of the sphere
initial_position = vector(0, 0, 0)

# Create a sphere at the initial position
s = sphere(pos=initial_position, radius=0.5, color=color.green)

# Function to handle mouse clicks
def on_click():
    # Check if the click is on the sphere
    if scene.mouse.pick == s:
        # Set the new position for the sphere where the mouse clicked
        s.pos = scene.mouse.pos
    print(scene.mouse.pick)

# Bind the click event to the on_click function
scene.bind('click', on_click)

while True:
    rate(30)
