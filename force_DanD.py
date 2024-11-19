import numpy as np
import matplotlib.pyplot as plt

# Initial charge positions
pos_pole = np.array([-10, 0])  # Positive charge
neg_pole = np.array([10, 0])   # Negative charge

dragging_pole = None

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

# Function to update the field plot
def update_field():
    plt.clf()
    x = np.linspace(-40, 40, 100)
    y = np.linspace(-30, 30, 100)
    X, Y = np.meshgrid(x, y)

    # Electric field from the positive and negative poles
    Ex1, Ey1 = electric_field(pos_pole, 1, X, Y)
    Ex2, Ey2 = electric_field(neg_pole, -1, X, Y)

    # Combine electric fields
    Ex = Ex1 + Ex2
    Ey = Ey1 + Ey2

    # Field strength for field line density
    E_magnitude = np.sqrt(Ex**2 + Ey**2)

    # Normalize vectors for quiver plot
    Ex_norm = Ex / E_magnitude
    Ey_norm = Ey / E_magnitude

    # Plot field lines
    plt.streamplot(X, Y, Ex, Ey, color=E_magnitude, linewidth=1, cmap='cool')
    plt.quiver(X[::5, ::5], Y[::5, ::5], Ex_norm[::5, ::5], Ey_norm[::5, ::5], color='black', scale=30)
    plt.scatter(*pos_pole, color='red', s=100, label='Positive charge (+)')
    plt.scatter(*neg_pole, color='blue', s=100, label='Negative charge (-)')
    
    # Add labels and legend
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title("Electric Field Lines and Force Vectors \n Clara's version")
    plt.legend()
    plt.grid()
    plt.axis('equal')
    plt.draw()

# Event handlers for dragging poles
def on_press(event):
    global dragging_pole
    if event.inaxes is not None:
        if np.linalg.norm(np.array([event.xdata, event.ydata]) - pos_pole) < 2:
            dragging_pole = 'pos'
        elif np.linalg.norm(np.array([event.xdata, event.ydata]) - neg_pole) < 2:
            dragging_pole = 'neg'

def on_release(event):
    global dragging_pole
    dragging_pole = None

def on_motion(event):
    global dragging_pole
    if dragging_pole is not None and event.inaxes is not None:
        if dragging_pole == 'pos':
            pos_pole[0] = event.xdata
            pos_pole[1] = event.ydata
        elif dragging_pole == 'neg':
            neg_pole[0] = event.xdata
            neg_pole[1] = event.ydata
        update_field()

# Set up the plot
fig, ax = plt.subplots(figsize=(10, 8))
update_field()

# Connect event handlers to the figure
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

plt.show()
