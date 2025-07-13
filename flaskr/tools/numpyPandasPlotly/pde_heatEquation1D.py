import numpy as np
import matplotlib.pyplot as plt

# solve PDE Heat Equation in 1D u(t, x): ∂u/∂t ​= κ*∂²𝑢/∂x² # pylint: disable=E2515

# Defining our problem
k = 110
length = 50 #mm
time = 4 #seconds
nodes = 20

# Initialization
dx = length / nodes
dt = 0.5 * dx**2 / k # γ=(k⋅dt)/(dx^2) <= 0.5 Courant-Friedrichs-Lewy (CFL) condition condition for stability
t_nodes = int(time/dt)

u = np.zeros(nodes) + 20 # Plate is initially as 20 degres C

# Boundary Conditions
u[0] = 100 # 100 degres C at x = 0
u[-1] = 100 # 100 degres C at x = L

# Visualizing with a plot
fig, axis = plt.subplots()
pcm = axis.pcolormesh([u], cmap='jet', vmin=0, vmax=100) # cmap=plt.cm.jet
plt.colorbar(pcm, ax=axis)
axis.set_ylim([-2, 3])

# Simulating
counter = 0

# u_new is the u(t+dt)
u_new = u.copy()

while counter < time :

    for i in range(1, nodes - 1):
        # Discretized Laplacian base on "Central difference Approximating Derivatives"
        # Discretized Laplacian | x=x_i: (u_{i-1} - 2u_i + u_{i+1}) / dx^2
        # see: pde Central difference Approximating.jpg
        u_new[i] = u[i] + dt * k * (u[i+1] - 2*u[i] + u[i-1]) / dx**2

    u = u_new.copy()
    counter += dt

    print("t: {:.3f} [s], Average temperature: {:.2f} Celcius".format(counter, np.average(u)))

    # Updating the plot

    pcm.set_array([u])
    axis.set_title("Distribution at t: {:.3f} [s].".format(counter))
    plt.pause(0.01)

plt.show()
