#doing this is like:
#https://www.youtube.com/watch?v=bZe5J8SVCYQ
from ploting import *
from symulation import *
from initial_conditions import *

# Main simulation loop
sym(pos,vel)

a = abs(max(positions[:, 0]) - min(positions[:, 0]))/2
b = abs(max(positions[:, 1]) - min(positions[:, 1]))/2
e_e = np.sqrt(1-(b**2/a**2))
print(a,b,e_e)
# Convert trajectory to array for plotting
print("initial v: ",v," m/s")

make_graf(positions)
# print(positions)