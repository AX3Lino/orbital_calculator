from ploting import *
from symulation import *
from initial_conditions import *

# Main simulation loop
 
positions,velocity,time = sym (Mothership.pos,Mothership.vel)
#print(positions,"positions", velocity,"velocity", time,"time") 
positions2,velocity2,time2 = sym (Pod.pos,Pod.vel)
# a = abs(max(positions[:,0]) - min(positions[:,0]))/2
# b = abs(max(positions[:,1]) - min(positions[:,1]))/2
# e_e = np.sqrt(1-(b**2/a**2))
# print(a,b,e_e)
# Convert trajectory to array for plotting
# print("initial v: ",v," m/s")
# delta_pos =np.array(positions[0,0]-positions2[0,0])
delta_pos =np.array([abs(np.array(positions[0,0]-positions2[0,0]))])
for i in range(len(positions2)):
    delta_pos=np.append(delta_pos,[abs(np.array(positions[i,0]-positions2[i,0]))])
    # print(delta_pos)
#TODO: make simulation actually 3D

# print(len(positions2),len(positions))

# make_graf(positions2)
# print(positions2,velocity2)
# print(delta_pos)

# file = open('delta_pos.txt', 'w')
# for lines in delta_pos:
    # file.write(f"{str(lines)}\n")
# file.close()