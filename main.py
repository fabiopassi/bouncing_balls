# *************************************
# ***         BOUNCING BALLS        ***
# *************************************

# IMPROVEMENTS TO DO:
#   -> Better collision detection: the actual one could not work for too high velocities (collision with walls are ok) 

# Importing modules
from utils.functions import *
import numpy as np
import matplotlib.pyplot as plt
import time
import random

# Box definition
y_floor = 0
x_right_wall = 3
x_left_wall = - x_right_wall
y_max = 2 * x_right_wall        

# Other variables
v_max = 7                       # Maximum initial velocity
g = 9.81                        # Gravitational acceleration
dt = 0.002                      # Timestep
steps = 5000                    # Simulation steps
N = 5                           # Number of balls

# Ball variables
traj = []
R = 0.2                                                                 # Radius
r = np.zeros((N,2))                                                     # Position
r[:,0] = (np.random.rand(N) - 0.5) * 2 * (x_right_wall - 2*R)           # x
r[:,1] = np.arange(1,N+1) * y_max/(2*(N+1))                             # y
v = np.zeros((N,2))                                                     # Velocity
v[:,0] = v_max * (np.random.rand(N) + np.ones(N)) / 2                   # vx                    
a = np.zeros((N,2))                                                     # Acceleration
a[:,1] = - g * np.ones(N)


# Time evolution
for t in range(steps) :

    # Velocity - Verlet
    r, v = velocity_verlet(r, v, a, dt)

    # Check for ball-ball collisions
    r,v = check_collision(r, v, R)

    # Check for rebound against walls
    r, v = check_rebound(r, v, a, y_floor, x_right_wall, x_left_wall, R)

    # Save coordinates
    traj.append(r)


# -------------------       Plot        --------------------------

# to run GUI event loop
plt.ion()
 
# here we are creating sub plots
figure, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim((x_left_wall, x_right_wall))
ax.set_ylim((y_floor, 2 * x_right_wall))
colors = [ ( "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) ) for i in range(N) ]

circ = []
for i in range(N) :
    tmp = plt.Circle((traj[0][i][0], traj[0][i][1]), R, color=colors[i])
    ax.add_artist(tmp)
    circ.append(tmp)

right_wall = ax.axvline(x = x_right_wall, ymin = y_floor, ymax = y_floor + 2 * x_right_wall)
left_wall = ax.axvline(x = x_left_wall,  ymin = y_floor, ymax = y_floor + 2 * x_right_wall)
floor = ax.axhline(y = y_floor, xmin = x_left_wall, xmax = x_right_wall)

plt.title("Bouncing balls", fontsize=20)
 
# setting x-axis label and y-axis label
plt.xlabel("x")
plt.ylabel("y")
 
# Loop
step_plot = 7
for k in range(0, len(traj), step_plot):

    # Update circle
    for circle in circ:
        circle.remove()
    circ = []
    for i in range(N) :
        tmp = plt.Circle((traj[k][i][0], traj[k][i][1]), R, color=colors[i])
        ax.add_artist(tmp)
        circ.append(tmp)
 
    # drawing updated values
    #figure.canvas.draw()
    figure.canvas.flush_events()
 
    time.sleep(0.008)

