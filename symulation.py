from initial_conditions import *


def gravitational_acceleration(r_temp,poss):
    return -G * M_e / r_temp ** 3 * poss

def atmospheric_drag(altitude,velo):
    v_temp = np.linalg.norm(velo)
    d= Drag(velo,v_temp,altitude) / mass
    # print(d)
    return -d

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
                # print(np.linalg.norm(vel))
                # print(t)
                orbits+=1
    print("time in 200-80km: ",science_time," s ", science_time/t*100, "% ", "time per orbit: ", science_time/orbits)
    print("orbits: ", orbits, "orbit time: ", t/orbits)


