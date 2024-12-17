import matplotlib.pyplot as plt
import matplotlib.patches as patches
from initial_conditions import *


def delta_distance (pos1,pos2):
    file = open('delta_pos.txt', 'w') #save position delta to file
    points = min(len(pos1),len(pos2))
    for i in range(points):
        delta_pos=abs(np.array(pos1[i,0]-pos2[i,0]))
        file.write(f"{str(delta_pos)}\n")
    file.close()


def make_graf(positions):
    fig,ax = plt.subplots()
    circle = patches.Circle((0,0),r_e/1000,fill=True,color='blue')
    ax.add_patch(circle)
    ax.plot(positions[:,0]/1000, positions[:,1]/1000,c='red', label='Orbit')
    plt.xlabel('X position (km)')
    plt.ylabel('Y position (km)')
    plt.title('Orbit Simulation')
    plt.axis('equal')
    plt.legend()
    plt.show()
