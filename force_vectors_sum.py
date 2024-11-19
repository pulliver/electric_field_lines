import numpy as np
import matplotlib.pyplot as plt

# Define the initial field space
x = np.linspace(-30, 30, 100)
y = np.linspace(-30, 30, 100)
X, Y = np.meshgrid(x, y)

# Define positions of fixed charges
pos_pole = np.array([-10, 0])  # Positive charge
neg_pole = np.array([10, 0])   # Negative charge

# Function to calculate electric field
def electric_field(pos, charge, x, y):
    rx = x - pos[0]
    ry = y - pos[1]
    r_squared = rx**2 + ry**2
    r = np.sqrt(r_squared)
    E_magnitude = charge / r_squared
    Ex = E_magnitude * rx / r
    Ey = E_magnitude * ry / r
    return Ex, Ey

# Combine electric field for streamplot
Ex1, Ey1 = electric_field(pos_pole, 1, X, Y)
Ex2, Ey2 = electric_field(neg_pole, -1, X, Y)
Ex = Ex1 + Ex2
Ey = Ey1 + Ey2

# Set up the figure and axes
fig, ax = plt.subplots(figsize=(10, 8))

# Plot the streamplot
stream = ax.streamplot(X, Y, Ex, Ey, color=np.sqrt(Ex**2 + Ey**2), linewidth=1, cmap='cool')
ax.scatter(*pos_pole, color='red', s=100, label='Positive charge (+)')
ax.scatter(*neg_pole, color='blue', s=100, label='Negative charge (-)')

# List to store dynamically added quivers
quivers = []

# Function to normalize and scale vectors
def normalize_vector(Ex, Ey, scale_length=5):
    magnitude = np.sqrt(Ex**2 + Ey**2)
    Ex_norm = (Ex / magnitude) * scale_length
    Ey_norm = (Ey / magnitude) * scale_length
    return Ex_norm, Ey_norm

# Function to handle mouse clicks
def on_click(event):
    global quivers
    if event.inaxes is not None:
        # Get the clicked position
        clicked_pos = np.array([event.xdata, event.ydata])

        # Calculate vectors
        Ex_repulsive, Ey_repulsive = electric_field(pos_pole, 1, clicked_pos[0], clicked_pos[1])
        Ex_attractive, Ey_attractive = electric_field(neg_pole, -1, clicked_pos[0], clicked_pos[1])

        # Sum of vectors
        Ex_sum = Ex_repulsive + Ex_attractive
        Ey_sum = Ey_repulsive + Ey_attractive

        # Normalize and scale the vectors for better visibility
        Ex_repulsive, Ey_repulsive = normalize_vector(Ex_repulsive, Ey_repulsive)
        Ex_attractive, Ey_attractive = normalize_vector(Ex_attractive, Ey_attractive)
        Ex_sum, Ey_sum = normalize_vector(Ex_sum, Ey_sum)

        # Remove existing quivers
        for q in quivers:
            q.remove()
        quivers = []

        # Plot the new vectors
        q_repulsive = ax.quiver(
            [clicked_pos[0]], [clicked_pos[1]],
            [Ex_repulsive], [Ey_repulsive],
            color='red', scale=1, scale_units='xy', label='Repulsive'
        )
        q_attractive = ax.quiver(
            [clicked_pos[0]], [clicked_pos[1]],
            [Ex_attractive], [Ey_attractive],
            color='blue', scale=1, scale_units='xy', label='Attractive'
        )
        q_sum = ax.quiver(
            [clicked_pos[0]], [clicked_pos[1]],
            [Ex_sum], [Ey_sum],
            color='green', scale=1, scale_units='xy', label='Sum'
        )

        # Store the new quivers for later removal
        quivers.extend([q_repulsive, q_attractive, q_sum])

        # Update the plot
        fig.canvas.draw()

# Connect the click event to the figure
fig.canvas.mpl_connect('button_press_event', on_click)

# Add labels and legend
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Electric Field with Interactive Charge Placement')
ax.legend()
ax.grid()
ax.axis('equal')

plt.show()
