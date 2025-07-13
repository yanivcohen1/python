import numpy as np
import matplotlib.pyplot as plt

# solve PDE Heat Equation in 2D u(t, x, y): ∂u/∂t ​= k(∂²𝑢/∂x² + ∂²𝑢/∂y²) # pylint: disable=E2515

# Defining our problem
k = 110
length = 50 #mm
time = 4 #seconds
nodes = 40

# Initialization
dx = length / nodes
dy = length / nodes

# γ=(k⋅dt)/(dx^2) <= 0.5 Courant-Friedrichs-Lewy (CFL) condition for stability
# we chooce γ=0.25 satisfying the (CFL) condition for stability
dt = min( dx**2 / (4 * k), dy**2 / (4 * k) )

t_nodes = int(time/dt)

u = np.zeros((nodes, nodes)) + 20 # Plate is initially as 20 degres C

# Boundary Conditions
u[0, :] = np.linspace(0, 100, nodes) # temp rising from 0 to 100 in x = 0
u[-1, :] = np.linspace(0, 100, nodes) # temp rising from 0 to 100 in x = L

u[:, 0] = np.linspace(0, 100, nodes) # temp rising from 0 to 100 in y = 0
u[:, -1] = np.linspace(0, 100, nodes) # temp rising from 0 to 100 in y = L

# Visualizing with a plot
fig, axis = plt.subplots()
pcm = axis.pcolormesh(u, cmap="jet", vmin=0, vmax=100) # cmap=plt.cm.jet
plt.colorbar(pcm, ax=axis)

# Simulating
counter = 0

# w is the memory for u[i+1 or j+1] that will not overide
# # u_new is the u(t+dt)
u_new = u.copy()

while counter < time :

    for i in range(1, nodes - 1):
        for j in range(1, nodes - 1):

            # Discretized Laplacian base on "Central difference Approximating Derivatives"
            # Discretized Laplacian | x=x_i: (u_{i-1} - 2u_i + u_{i+1}) / dx^2
            # see: pde Central difference Approximating.jpg
            dd_ux = (u[i+1, j] - 2*u[i, j] + u[i-1, j]) / dx**2
            # Discretized Laplacian | y=y_i: (u_{i-1} - 2u_i + u_{i+1}) / dy^2
            # see: pde Central difference Approximating.jpg
            dd_uy = (u[i, j+1] - 2*u[i, j] + u[i, j-1]) / dy**2

            # [∂u(t+1) - ∂u(t)]/∂t ​= ∂²𝑢/∂x² + ∂²𝑢/∂y²
            # dx = dy; dt = min( dx**2 / (4 * k) )
            u_new[i, j] = u[i, j] + dt * k * (dd_ux + dd_uy)

    u = u_new.copy()
    counter += dt

    print("t: {:.3f} [s], Average temperature: {:.2f} Celcius".format(counter, np.average(u)))

    # Updating the plot

    pcm.set_array(u)
    axis.set_title("Distribution at t: {:.3f} [s].".format(counter))
    plt.pause(0.01)

plt.show()
