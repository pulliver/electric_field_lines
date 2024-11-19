import numpy as np
import matplotlib.pyplot as plt

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

# Compute the electric field strength for field line density
E_magnitude = np.sqrt(Ex**2 + Ey**2)

# Normalize vectors for quiver plot
Ex_norm = Ex / E_magnitude
Ey_norm = Ey / E_magnitude

# Plot the field lines using streamplot
plt.figure(figsize=(10, 8))
plt.streamplot(X, Y, Ex, Ey, color=E_magnitude, linewidth=1, cmap='cool')
plt.quiver(X[::5, ::5], Y[::5, ::5], Ex_norm[::5, ::5], Ey_norm[::5, ::5], color='black', scale=30)

# Plot the charges
plt.scatter(*pos_pole, color='red', s=100, label='Positive charge (+)')
plt.scatter(*neg_pole, color='blue', s=100, label='Negative charge (-)')

# Add labels and legend
plt.xlabel('x')
plt.ylabel('y')
plt.title('Electric Field Lines and Force Vectors')
plt.legend()
plt.grid()
plt.axis('equal')
plt.colorbar(label='Electric Field Magnitude')
plt.show()
