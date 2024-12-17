from initial_conditions import *
from nrlmsis_calculator import *

def gravitational_acceleration(r_temp,poss):
    return -G * M_e / r_temp ** 3 * poss

def atmospheric_drag(t, altitude_km,velo,mass,A):
    v_temp = np.linalg.norm(velo)
    ro = get_atmospheric_data(t, altitude_km,0,0)[1]
    d= Drag(velo,v_temp,ro,A) / mass
    return -d

def sym(satellite):
    orbit = []
    orbits = 0
    ionosphere_time = 0
    t=0
    pos = satellite.pos
    vel = satellite.vel
    positions=np.array(satellite.pos, ndmin=2)
    velocity = np.array(satellite.vel, ndmin=2)
    time=np.array(t)
    for i in range(n_steps):
        r_temp = np.linalg.norm(satellite.pos)
        altitude = (r_temp - r_e)
        acc = gravitational_acceleration(r_temp,pos) + atmospheric_drag(t,altitude/1000, vel,satellite.mass,satellite.A)

        # Update velocity and position using Euler method
        vel += acc * dt
        pos += vel * dt
        t +=dt
        positions=np.append(positions,[pos],axis=0)
        velocity=np.append(velocity,[vel],axis=0)
        time=np.append(time,t)

        if r_temp < r_e:
            print('flight time:',i / 3600 * dt, " h")
            print("FALL")
            break
        if 200 > altitude/1000 > 120:
            ionosphere_time+=dt
        if i:
            if positions[i - 1,1] < 0 < positions[i,1]:
                orbits+=1
                break
                if orbit:
                    orbit.append(t-sum(orbit))
                else:
                    orbit.append(t)
    # print("time in 200-80km: ", ionosphere_time, " s ", ionosphere_time / t * 100, "% ", "time per orbit: ",ionosphere_time / orbits)
    # print("orbits: ", orbits, "orbit time: ", orbit)
    return positions, velocity, time




