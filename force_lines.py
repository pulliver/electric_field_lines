import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# Define the Cartesian space
x = np.linspace(-30, 30, 100)
y = np.linspace(-30, 30, 100)
X, Y = np.meshgrid(x, y)

# Define the positions of the positive and negative poles
pos_pole = np.array([-10, 0])  # Positive charge
neg_pole = np.array([10, 0])   # Negative charge

# Define the electric field function
def electric_field(pos, charge, x, y):
    rx = x - pos[0]
    ry = y - pos[1]
    r_squared = rx**2 + ry**2
    r_squared[r_squared == 0] = 1e-9  # Avoid division by zero
    r = np.sqrt(r_squared)
    E_magnitude = charge / r_squared  # Coulomb's law
    Ex = E_magnitude * rx / r
    Ey = E_magnitude * ry / r
    return Ex, Ey

# Electric field from the positive pole (charge = +1)
Ex1, Ey1 = electric_field(pos_pole, 1, X, Y)

# Electric field from the negative pole (charge = -1)
Ex2, Ey2 = electric_field(neg_pole, -1, X, Y)

# Combine the electric fields
Ex = Ex1 + Ex2
Ey = Ey1 + Ey2

# Compute the electric field strength for coloring
E_magnitude = np.sqrt(Ex**2 + Ey**2)
print(f'magnitude: {E_magnitude}')
# Adjust normalization to match the range of E_magnitude
# vmin = E_magnitude.min()  # Minimum value of the magnitude
# vmax = E_magnitude.max()  # Maximum value of the magnitude

# Apply a logarithmic transformation to spread out values
E_magnitude_log = np.log1p(E_magnitude)  # log1p is log(1 + x), avoids issues with very small values
vmin = E_magnitude_log.min()
vmax = E_magnitude_log.max()
print(f'max {vmax}, min {vmin}')
norm = Normalize(vmin=vmin, vmax=vmax)
cmap = plt.cm.plasma

# Map the magnitudes to RGBA colors
colors = cmap(norm(E_magnitude[::5, ::5]))
colors_flat = colors.reshape(-1, 4)  # Flatten the 2D color array to 1D

# Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 8))

# Plot the field lines using streamplot
stream = ax.streamplot(X, Y, Ex, Ey, color=E_magnitude, linewidth=1, cmap='cool')

# Add quiver plot
ax.quiver(
    X[::5, ::5].flatten(), Y[::5, ::5].flatten(),  # Flatten X and Y
    Ex[::5, ::5].flatten(), Ey[::5, ::5].flatten(),
    color=colors_flat,  # Use the flattened color array
    scale=1e6  # Adjust scale for visualization
)

# Plot the charges
ax.scatter(*pos_pole, color='red', s=100, label='Positive charge (+)')
ax.scatter(*neg_pole, color='blue', s=100, label='Negative charge (-)')

# Add labels and legend
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Electric Field Lines and Colored Force Vectors')
ax.legend()
ax.grid()
ax.axis('equal')

# Add a colorbar for the streamplot
cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, label='Electric Field Magnitude')

plt.show()
