import pandas as pd
import numpy as np
import astropy.constants as constants
import astropy as astro

#TODO: import pod r,v from desmos

atmo_file  = pd.read_csv("atmo_0_to_1000.txt", sep=r"\s+", engine="python")

G = constants.G.value # gravitational constant
M_e = constants.M_earth.value  # mass earth [kg]
r_e = constants.R_earth.value  # radius earth [m]

# Ro = lambda h_fun: 0 if h_fun > 1_000_000 else atmo_file["air(kg/m3)"][int(h_fun/1000)] # density based on height [kg/m3]
Drag = lambda vel_fun, v_fun, ro_fun, A_fun: A_fun  * 0.5* ro_fun * vel_fun * v_fun # drag vector [m/s2]
V = lambda r_fun: np.sqrt(G * M_e / r_fun) # velocity for circular orbit
V0 = lambda t_fun,l_low,l_high: np.sqrt((r_e+l_high)**2-(r_e+l_low)**2)/t_fun
#Tau = lambda :2*np.pi*pow(pow(r,3) / (G * M_e), 0.5) #time circular orbit

# Cd = 1 # drag coefficient

dt = 1  # Time step (s)
total_time = 200000.0  # Total simulation time (s)
n_steps = int(total_time / dt)

class Mothership:
    H=300e3
    mass = 200
    A = 0.5 * 0.5
    Cd = 1

    r = H + r_e
    v = V(r) * 1.00
    pos = np.array([r, 0])  # Initial position (m)
    vel = np.array([0.0, v])
    # print(v)


class Pod:
    H = 120e3
    mass = 5
    A = 0.2 *0.2
    Cd = 1

    r = H + r_e
    v = V(r) * 1.007
    v = 7.66834622e+03
    r = 300e3 +r_e
    pos = np.array([r, 0])  # Initial position (m)
    vel = np.array([0.0, v])
    # print(v)
