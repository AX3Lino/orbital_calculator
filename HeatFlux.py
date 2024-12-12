from nrlmsis_calculator import *
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class ProbeAnalysis:
    def __init__(self, shape='sphere', volume=0.001):  # volume in m³ (1L = 0.001m³)
        self.shape = shape
        self.volume = volume
        self.characteristic_length = self._calculate_characteristic_length()
        
    def _calculate_characteristic_length(self):
        """Calculate characteristic length based on shape and volume"""
        if self.shape == 'sphere':
            # For sphere, characteristic length is diameter
            return 2 * (3 * self.volume / (4 * np.pi))**(1/3)
        elif self.shape == 'square':
            # For cube, characteristic length is side length
            return self.volume**(1/3)
        elif self.shape == 'double_cone':
            # Assuming height = 2*base radius for double cone
            radius = (3 * self.volume / (2 * np.pi))**(1/3)
            return 4 * radius  # Total length
        return None

    def calculate_drag_coefficient(self, mach_number):
        """Calculate drag coefficient based on shape and Mach number"""
        if self.shape == 'sphere':
            return 0.47 if mach_number < 1 else 0.92
        elif self.shape == 'square':
            return 1.05 if mach_number < 1 else 1.5
        elif self.shape == 'double_cone':
            return 0.5 if mach_number < 1 else 0.8
        return None

    def calculate_reference_area(self):
        """Calculate reference area based on shape"""
        if self.shape == 'sphere':
            radius = (3 * self.volume / (4 * np.pi))**(1/3)
            return np.pi * radius**2
        elif self.shape == 'square':
            side = self.volume**(1/3)
            return side**2
        elif self.shape == 'double_cone':
            radius = (3 * self.volume / (2 * np.pi))**(1/3)
            return np.pi * radius**2
        return None

    def calculate_heat_flux(self, velocity, density, position=None):
        """
        Calculate heat flux using Sutton-Graves equation
        position: normalized position along the body (0 to 1)
        """
        k = 1.742e-4  # Sutton-Graves constant
        nose_heat_flux = k * np.sqrt(density / self.characteristic_length) * velocity**3

        if position is not None:
            # Distribute heat flux along the body based on position
            if self.shape == 'sphere':
                # Spherical distribution
                theta = position * np.pi
                return nose_heat_flux * np.cos(theta)
            elif self.shape == 'square':
                # Simple linear reduction
                return nose_heat_flux * (1 - position)
            elif self.shape == 'double_cone':
                # Conical distribution with peak at nose
                return nose_heat_flux * np.exp(-2 * position)
        return nose_heat_flux

def simulate_orbit(probe, initial_altitude=200000, duration_hours=24):
    """Simulate orbital decay and heating"""
    # Orbital parameters
    R_earth = 6371000  # Earth radius in meters
    g0 = 9.81  # m/s²
    mass = 1.0  # kg (assumed)
    
    # Time array
    t = np.linspace(0, duration_hours * 3600, 1000)
    
    # Initial conditions [r, v, θ]
    y0 = [R_earth + initial_altitude, np.sqrt(g0 * R_earth**2 / (R_earth + initial_altitude)), 0]
    
    def orbital_decay(y, t):
        r, v, theta = y
        
        # Get atmospheric density at current altitude
        altitude_km = (r - R_earth) / 1000
        _, density = get_atmospheric_data(datetime.now(), altitude_km, 0, 0)
        
        # Calculate drag
        Cd = probe.calculate_drag_coefficient(v / 340)  # Approximate Mach number
        A = probe.calculate_reference_area()
        drag = -0.5 * density * v**2 * Cd * A / mass
        
        # Equations of motion
        dr_dt = v * np.sin(theta)
        dv_dt = drag - g0 * (R_earth/r)**2 * np.sin(theta)
        dtheta_dt = v * np.cos(theta) / r
        
        return [dr_dt, dv_dt, dtheta_dt]
    
    # Solve orbital equations
    solution = odeint(orbital_decay, y0, t)
    
    return t, solution

def plot_results(probe, t, solution):
    """Generate plots for the analysis"""
    # Calculate derived quantities
    altitudes = solution[:, 0] - 6371000  # Convert radius to altitude
    velocities = solution[:, 1]
    
    # Calculate heat flux along the trajectory
    heat_fluxes = []
    for i in range(len(t)):
        _, density = get_atmospheric_data(datetime.now(), altitudes[i]/1000, 0, 0)
        heat_fluxes.append(probe.calculate_heat_flux(velocities[i], density))
    
    # Plot results
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Altitude vs time
    ax1.plot(t/3600, altitudes/1000)
    ax1.set_xlabel('Time (hours)')
    ax1.set_ylabel('Altitude (km)')
    ax1.set_title('Orbital Decay')
    
    # Heat flux vs time
    ax2.plot(t/3600, np.array(heat_fluxes)/1e6)
    ax2.set_xlabel('Time (hours)')
    ax2.set_ylabel('Heat Flux (MW/m²)')
    ax2.set_title('Heat Flux vs Time')
    
    # Heat flux distribution
    positions = np.linspace(0, 1, 100)
    distributed_flux = [probe.calculate_heat_flux(velocities[0], 
                                                get_atmospheric_data(datetime.now(), 
                                                                   altitudes[0]/1000, 0, 0)[1],
                                                position) for position in positions]
    ax3.plot(positions, np.array(distributed_flux)/1e6)
    ax3.set_xlabel('Normalized Position')
    ax3.set_ylabel('Heat Flux (MW/m²)')
    ax3.set_title('Heat Flux Distribution')
    
    # Accumulated heat
    accumulated_heat = np.cumsum(np.array(heat_fluxes) * probe.calculate_reference_area() * (t[1]-t[0]))
    ax4.plot(t/3600, accumulated_heat/1e6)
    ax4.set_xlabel('Time (hours)')
    ax4.set_ylabel('Accumulated Heat (MJ)')
    ax4.set_title('Accumulated Heat')
    
    plt.tight_layout()
    return fig

# Example usage:
if __name__ == "__main__":
    shapes = ['sphere', 'square', 'double_cone']
    for shape in shapes:
        probe = ProbeAnalysis(shape=shape)
        t, solution = simulate_orbit(probe)
        fig = plot_results(probe, t, solution)
        plt.savefig(f'{shape}_analysis.png')
        plt.close()


probe = ProbeAnalysis(shape='sphere')  # or 'square' or 'double_cone'
t, solution = simulate_orbit(probe)
plot_results(probe, t, solution)
plt.show()