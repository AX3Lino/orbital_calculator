from initial_conditions import *
from nrlmsis_calculator import *

def gravitational_acceleration(r_temp,poss):
    return -G * M_e / r_temp ** 3 * poss

def atmospheric_drag(t, altitude_km,velo):
    v_temp = np.linalg.norm(velo)
    ro = get_atmospheric_data(t, altitude_km,0,0)[1]
    d= Drag(velo,v_temp,ro) / mass
    return -d

def sym(pos,vel):
    orbit = []
    orbits = 0
    ionosphere_time = 0
    t=0
    positions=np.array(pos,ndmin=2)
    velocity = np.array(vel,ndmin=2)
    time=np.array(t)
    # positions.append(pos)
    # velocity.append(vel)
    # time.append(t)
    for i in range(n_steps):
        positions[i] = pos
        # Compute acceleration due to gravity
        # print(gravitational_acceleration(pos))
        # print(atmospheric_drag(pos,vel))
        r_temp = np.linalg.norm(pos)
        altitude = (r_temp - r_e)
        acc = gravitational_acceleration(r_temp,pos) + atmospheric_drag(t,altitude/1000, vel)

        # Update velocity and position using Euler method
        vel += acc * dt
        pos += vel * dt
        t +=dt
        positions=np.append(positions,[pos],axis=0)
        velocity=np.append(velocity,[vel],axis=0)
        time=np.append(time,t)

        if r_temp < r_e:
            # positions[i+1]=np.zeros(2)
            print('flight time:',i / 3600 * dt, " h")
            print("FALL")
            break
        if 200 > altitude/1000 > 120:
            ionosphere_time+=dt
        if i:
            if positions[i - 1,1] < 0 < positions[i,1]:
            # if positions[i-1,1] > 0 > positions[i,1]:
                # print(np.linalg.norm(vel))
                # orbit.append(t)
                orbits+=1
                # print(positions[i],velocity[i])
                break
                if orbit:
                    orbit.append(t-sum(orbit))
                else:
                    orbit.append(t)
    # print("time in 200-80km: ", ionosphere_time, " s ", ionosphere_time / t * 100, "% ", "time per orbit: ",ionosphere_time / orbits)
    # print("orbits: ", orbits, "orbit time: ", orbit)
    return positions, velocity, time




