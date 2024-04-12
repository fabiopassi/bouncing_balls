""" This module contains all the functions for ... script """

# Importing modules
import numpy as np
from numba import njit

# Functions

@njit
def velocity_verlet (x, v, a, dt) :
    """ This function upgrades positions and velocities of the particles using the velocity
        verlet algorithm. This function makes use of calculate_forces """

    v_dt_2 = np.zeros(v.shape)

    v_dt_2 = v + 0.5 * a * dt                       # Update velocities pt.1
    x = x + v_dt_2 * dt                             # Update position
    v = v_dt_2 + 0.5 * a * dt                       # Update velocities pt.2
    
    return x, v



@njit
def check_collision(r, v, R) :

    for i in range(r.shape[0]) :
        for j in range(i+1, r.shape[0]) :
            # Check for collision
            dr = r[i,:] - r[j,:]
            if np.sqrt( np.square(dr).sum() ) < 2 * R :
                # Store old velocities
                v_i_old = v[i,:].copy()
                v_j_old = v[j,:].copy()
                # Change velocity according to conservation laws
                v[i] = v_i_old - ( ((v_i_old-v_j_old) * (r[i]-r[j])).sum() ) / (np.square(r[i]-r[j]).sum()) * (r[i]-r[j])
                v[j] = v_j_old - ( ((v_j_old-v_i_old) * (r[j]-r[i])).sum() ) / (np.square(r[i]-r[j]).sum()) * (r[j]-r[i])
    
    return r,v



@njit
def check_rebound(r, v, a, y_floor, x_right_wall, x_left_wall, R) :

    for i in range(r.shape[0]) :
        # Floor
        if r[i,1] - y_floor < R :
            # Take into account floor penetration
            penetration_length = y_floor - r[i,1] + R
            r[i,1] += 2 * penetration_length
            # Invert motion and correct extra velocity increase due to gravity
            v_impact = np.sqrt( np.square(v[i,1]) - 2 * abs(a[i,1]) * penetration_length )
            v[i,1] = - v_impact
            v[i,1] = np.sqrt(np.square(v[i,1]) - 2 * abs(a[i,1]) * penetration_length )

        # Left wall
        if x_left_wall - r[i,0] > - R :
            # Take into account wall penetration
            penetration_length = x_left_wall - r[i,0] + R
            r[i,0] += 2 * penetration_length
            # Invert motion
            v[i,0] *= -1

        # Right wall
        if (x_right_wall - r[i,0]) < R :
            # Take into account wall penetration
            penetration_length = r[i,0] - x_right_wall + R
            r[i,0] -= 2 * penetration_length
            # Invert motion
            v[i,0] *= -1

    return r, v

