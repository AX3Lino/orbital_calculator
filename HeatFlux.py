from main import *
from nrlmsis_calculator import get_atmospheric_data as nrlmsis
from Heat_profile import *
import numpy as np
import matplotlib.pyplot as plt


# Constants
C_IRON = 449  # Heat capacity of iron in J/(kg·K)
volume=0.001
INITIAL_TEMPERATURE = 300  # Initial temperature in Kelvin (27°C)
IRON_DENSITY = 7850  # Density of the object in kg/m^3
thickness = 0.002 #thicken in m
# Setup for the simulation
shape = Shape(name="double_cone",volume=volume)  # Example: sphere with 0.001 m³ volume

# Precompute heat flux, accumulated heat, and temperature
heat_fluxes = []
accumulated_heat = []
temperatures = []
current_accumulated_heat = 0

for pos, vel, t in zip(positions2, velocity2, time2):
    # Get atmospheric properties
    print
    temperature, density = nrlmsis(float(t), (pos[0]-r_e)/1000, 0, 0)

    # Compute heat flux
    heat_flux = shape.calculate_heat_flux_coefficient(density, vel[1])

    # Update accumulated heat
    current_accumulated_heat += heat_flux * shape.reference_area * thickness * dt

    # Compute temperature
    current_temperature = INITIAL_TEMPERATURE + (current_accumulated_heat / (volume*IRON_DENSITY * C_IRON))

    heat_fluxes.append(heat_flux)
    accumulated_heat.append(current_accumulated_heat)
    temperatures.append(current_temperature)

# Plot results
fig, axs = plt.subplots(3, 1, figsize=(10, 12))

# Heat flux vs time
axs[0].plot(time2, heat_fluxes, label="Heat Flux")
axs[0].set_title("Heat Flux vs Time")
axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("Heat Flux (W/m²)")
axs[0].grid()
axs[0].legend()

# Accumulated heat vs time
axs[1].plot(time2, accumulated_heat, label="Accumulated Heat", color="orange")
axs[1].set_title("Accumulated Heat vs Time")
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Accumulated Heat (J)")
axs[1].grid()
axs[1].legend()

# Temperature vs time
axs[2].plot(time2, temperatures, label="Temperature", color="red")
axs[2].set_title("Temperature vs Time")
axs[2].set_xlabel("Time (s)")
axs[2].set_ylabel("Temperature (K)")
axs[2].grid()
axs[2].legend()

plt.tight_layout()
plt.show()
