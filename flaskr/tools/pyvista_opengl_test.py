import json
import time
import numpy as np
import pyvista as pv

# --- Simulation Settings ---
NUM_POINTS = 64
RADIUS = 5


def simulate_sensor_data(frame):
    angle = np.linspace(0, 2 * np.pi, NUM_POINTS)
    x = RADIUS * np.cos(angle + frame * 0.1)
    y = RADIUS * np.sin(angle + frame * 0.1)
    # The sinus wave on the Z axis
    z = np.sin(angle * 3 + frame * 0.2) * 2

    points = np.column_stack((x, y, z))
    return json.dumps(points.tolist())


# --- PyVista Setup ---
plotter = pv.Plotter()
cloud = pv.PolyData(np.zeros((NUM_POINTS, 3)))

# Add a floor or axes to keep spatial context
plotter.add_axes()
plotter.add_mesh(cloud, render_points_as_spheres=True, point_size=10, color="lime")

# FIX: Manually set the camera to look at the center from a distance
# Position: (x, y, z), Focal Point: (0, 0, 0), View Up: (0, 0, 1)
plotter.camera_position = [(15, 15, 15), (0, 0, 0), (0, 0, 1)]

plotter.show(interactive_update=True)

frame_counter = 0

while True:
    raw_data = simulate_sensor_data(frame_counter)
    data = json.loads(raw_data)
    pts = np.array(data)

    cloud.points = pts

    # Optional: Uncomment the line below if you want the camera to
    # auto-adjust to the data every frame (can be jittery)
    # plotter.reset_camera()

    plotter.update()

    frame_counter += 1
    time.sleep(0.01)
