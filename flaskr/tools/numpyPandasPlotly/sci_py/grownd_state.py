import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# ground state is whare n=1 k=n*pi whare k is ψ" = kψ


# Define the Schrödinger equation
def schroedinger_eqn(x, y, E, g):
    psi, phi = y
    dpsi_dx = phi
    dphi_dx = (0.5 * x**2 + g * x**4 - E) * psi
    return [dpsi_dx, dphi_dx]

# Shooting method
def shoot(E, g):
    sol = solve_ivp(schroedinger_eqn, [10, 0], [0, -0.1], args=(E, g), dense_output=True)
    return sol.sol(0)[0]

# Find the ground state energy by varying E and looking for zero crossing
def find_ground_state(g):
    E_values = np.linspace(0, 10, 100)
    psi_at_origin = []

    for E in E_values:
        psi_at_origin.append(shoot(E, g))

    # Find zero crossing
    zero_crossings = np.where(np.diff(np.sign(psi_at_origin)))[0]
    if len(zero_crossings) == 0:
        return None
    return E_values[zero_crossings[0]]

# Plot ground state energy as a function of g
g_values = np.linspace(1, 5, 5)
ground_state_energies = []
g_vals = []

for g in g_values:
    E_ground = find_ground_state(g)
    if E_ground is not None:
        ground_state_energies.append(E_ground)
        g_vals.append(g)

plt.plot(g_vals, ground_state_energies, marker='o')
plt.xlabel('g')
plt.ylabel('Ground State Energy E')
plt.title('Ground State Energy vs Anharmonic Term g, where $\psi=0$')
plt.grid(True)
plt.show()
