#doing this is like:
#https://www.youtube.com/watch?v=bZe5J8SVCYQ
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import astropy.constants as const
import pandas as pd

atmo_file  = pd.read_csv("atmo_0_to_1000.txt", sep=r"\s+", engine="python")

def make_graf(positions):
    fig,ax = plt.subplots()
    circle = patches.Circle((0,0),r_e/1000,fill=True,color='blue')
    ax.add_patch(circle)
    ax.plot(positions[:, 0]/1000, positions[:, 1]/1000,c='red', label='Orbit')
    plt.xlabel('X position (m)')
    plt.ylabel('Y position (m)')
    plt.title('Orbit Simulation')
    plt.axis('equal')
    plt.legend()
    plt.show()


#Ms 200
Cd = 1 # drag coefficient
# print(H)
G = const.G.value # gravitational constant
M_e = const.M_earth.value  # mass earth [kg]
r_e = const.R_earth.value  # radius earth [m]



Ro = lambda h_fun: 0 if h_fun > 1_000_000 else atmo_file["air(kg/m3)"][int(h_fun/1000)] # density based on height [kg/m3]
Drag = lambda vel_fun, v_fun, h_fun: A * Ro(h_fun) * 0.5 * vel_fun * v_fun # drag vector [m/s2]
V = lambda r_fun: np.sqrt(G * M_e / r_fun) # velocity for circular orbit
Tau = lambda :2*np.pi*pow(pow(r,3) / (G * M_e), 0.5) #time circular orbit
# Tau_e = sqrt(4*pi^2*a^3/G*m_e)  a=sami-major axis

# a_grav = m_e * G / H ** 2
# x = 0
# alfa = np.arcsin(x / H)
# print(alfa)
# print(a_grav)
# print(np.cos(alfa)*a_grav)


H=120e3 # initial altitude above ground [m] qs
H2=300e3 # initial altitude above ground [m] ms

mass = 1 #kg    qs
# mass = 100 #kg  ms

A = 0.1 *0.1 #m^2   qs
# A = 0.2 *0.2 #m^2   qs 2x2
# A = 0.5 *0.5 #m^2   ms

r = H + r_e
r2 = H2 + r_e
# print(r)

# v = V(r)*1.2
v = V(r)*1.007 #qs
# v = V(r)*1.01 #qs 2x2


a_drag = Drag(v,v,H)
print(V(r2))
# print(V(),"m/s")
# print(Tau(),"s")
print("drag ",a_drag,"m/s^2")
# print(a_drag*mass,"N")


# print("terminal velocity: ",v,"m/s^2")
# initial_v = V()


pos = np.array([-r, 0])  # Initial position (m)
vel = np.array([0.0, v])
dt = 1  # Time step (s)
total_time = 200000.0  # Total simulation time (s)
n_steps = int(total_time / dt)

# Storage for positions
positions = np.zeros((n_steps, 2))
time = np.zeros(n_steps)

def gravitational_acceleration(r_temp,poss):
    return -G * M_e / r_temp ** 3 * poss

def atmospheric_drag(altitude,velo):
    v_temp = np.linalg.norm(velo)
    d= Drag(velo,v_temp,altitude)
    # print(d)
    return -d

# Main simulation loop

def sym(pos,vel):
    orbits = 0
    science_time = 0
    t=0
    for i in range(n_steps):
        positions[i] = pos
        # Compute acceleration due to gravity
        # print(gravitational_acceleration(pos))
        # print(atmospheric_drag(pos,vel))
        r_temp = np.linalg.norm(pos)
        altitude = (r_temp - r_e)
        acc = gravitational_acceleration(r_temp,pos) + atmospheric_drag(altitude, vel)

        # Update velocity and position using Euler method
        vel += acc * dt
        pos += vel * dt
        t +=dt
        if r_temp < r_e:
            # positions[i+1]=np.zeros(2)
            print('flight time:',i / 3600 * dt, " h")
            break
        # print(altitude/1000)
        if 200 > altitude/1000 > 80:
            science_time+=dt
        if i:
            if positions[i - 1,1] < 0 < positions[i,1]:
                print(np.linalg.norm(vel))
                orbits+=1



    print("time in 200-80km: ",science_time," s ", science_time/total_time*100, "% ", "time per orbit: ", science_time/orbits)
    print("orbits: ", orbits, "orbit time: ", total_time/orbits)


sym(pos,vel)

a = abs(max(positions[:, 0]) - min(positions[:, 0]))/2
b = abs(max(positions[:, 1]) - min(positions[:, 1]))/2
e_e = np.sqrt(1-(b**2/a**2))
print(a,b,e_e)
# Convert trajectory to array for plotting
print("initial v: ",v," m/s")
# make_graf(positions)
# print(positions)