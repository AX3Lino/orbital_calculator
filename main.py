from output import *
from symulation import *
from initial_conditions import *


# Main simulation loop
positions1,velocity,time1 = sym (Mothership)
positions2,velocity2,time2 = sym (Pod)

#TODO: make simulation actually 3D
if __name__ == "__main__":
    make_graf(positions1)
    make_graf(positions2)
    delta_distance(positions1, positions2)

    plt.plot(time1, (positions1[:, 0]-r_e) / 1000, label="Mothership")
    plt.xlabel("Time (s)")
    plt.ylabel("Altitud (km)")
    plt.plot(time2, (positions2[:, 0]-r_e) / 1000, label="Pod")  
    plt.xlabel("Time (s)")
    plt.ylabel("Altitud (km)")
    plt.legend()
    plt.show()
# make_graf(positions1)
# make_graf(positions2)
# delta_distance(positions1, positions2)


