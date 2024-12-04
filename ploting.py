import matplotlib.pyplot as plt
import matplotlib.patches as patches
import astropy.constants as const
r_e = const.R_earth.value  # radius earth [m]

def make_graf(positions):
    fig,ax = plt.subplots()
    circle = patches.Circle((0,0),r_e/1000,fill=True,color='blue')
    ax.add_patch(circle)
    ax.plot(positions[:, 0]/1000, positions[:, 1]/1000,c='red', label='Orbit')
    plt.xlabel('X position (km)')
    plt.ylabel('Y position (km)')
    plt.title('Orbit Simulation')
    plt.axis('equal')
    plt.legend()
    plt.savefig('orbit_pod.png')
    plt.show()
