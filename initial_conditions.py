import pandas as pd
import numpy as np
import astropy.constants as const

atmo_file  = pd.read_csv("atmo_0_to_1000.txt", sep=r"\s+", engine="python")

G = const.G.value # gravitational constant
M_e = const.M_earth.value  # mass earth [kg]
r_e = const.R_earth.value  # radius earth [m]


Ro = lambda h_fun: 0 if h_fun > 1_000_000 else atmo_file["air(kg/m3)"][int(h_fun/1000)] # density based on height [kg/m3]
Drag = lambda vel_fun, v_fun, h_fun: A * Ro(h_fun) * 0.5 * vel_fun * v_fun # drag vector [m/s2]
V = lambda r_fun: np.sqrt(G * M_e / r_fun) # velocity for circular orbit
V0 = lambda t_fun,l_low,l_high: np.sqrt((r_e+l_high)**2-(r_e+l_low)**2)/t_fun
Tau = lambda :2*np.pi*pow(pow(r,3) / (G * M_e), 0.5) #time circular orbit
# Tau_e = sqrt(4*pi^2*a^3/G*m_e)  a=sami-major axis


Cd = 1 # drag coefficient

# H=120e3 # initial altitude above ground [m] qs
H2=300e3 # initial altitude above ground [m] ms

# mass = 1 #kg    qs
mass = 200 #kg  ms

# A = 0.1 *0.1 #m^2   qs
# A = 0.2 *0.2 #m^2   qs 2x2
A = 0.5 *0.5 #m^2   ms

# r = H + r_e
r = H2 + r_e
# print(r)
# print(V0(30*60,120,200))
v = V(r)*1.005
# v = V(r)*1.007 #qs
# v = V(r)*1.01 #qs 2x2


# a_drag = Drag(v,v,H)/mass
# print(v)
print(v)
# print(V(),"m/s")
# print(Tau(),"s")
# print("drag ",a_drag,"m/s^2")
# print(a_drag*mass,"N")


# print("terminal velocity: ",v,"m/s^2")
# initial_v = V()


pos = np.array([r, 0])  # Initial position (m)
vel = np.array([0.0, v])
dt = 1  # Time step (s)
total_time = 200000.0  # Total simulation time (s)
n_steps = int(total_time / dt)

# Storage for positions
positions = np.zeros((n_steps, 2))
time = np.zeros(n_steps)
