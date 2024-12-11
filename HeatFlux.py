import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Literal, Dict

@dataclass
class MaterialProperties:
    name: str
    density: float  # kg/m³
    specific_heat: float  # J/(kg·K)
    thermal_conductivity: float  # W/(m·K)
    melting_point: float  # K

@dataclass
class ProbeConfig:
    shape: Literal['sphere', 'cube', 'cone', 'double_cone']
    diameter: float  # meters
    velocity: float  # m/s
    entry_angle: float = -5   # degrees
    material: MaterialProperties = None

def get_materials_database() -> Dict[str, MaterialProperties]:
    """Database of common heat shield materials"""
    return {
        'carbon_phenolic': MaterialProperties(
            name='Carbon Phenolic',
            density=1900,
            specific_heat=1600,
            thermal_conductivity=0.5,
            melting_point=3000
        )
    }

def get_shape_coefficients(shape: str) -> dict:
    """Get aerodynamic coefficients for different shapes"""
    coefficients = {
        'sphere': {
            'drag': 0.47,
            'heat_factor': 1.0,  # Reference value
            'pressure_coefficient': 1.0
        },
        'cube': {
            'drag': 1.05,
            'heat_factor': 1.4,  # Higher heating due to sharp edges
            'pressure_coefficient': 1.4
        },
        'cone': {
            'drag': 0.50,
            'heat_factor': 0.8,  # Lower heating due to oblique shock
            'pressure_coefficient': 0.8
        },
        'double_cone': {
            'drag': 0.55,
            'heat_factor': 0.7,  # Even lower heating due to double shock
            'pressure_coefficient': 0.7
        }
    }
    return coefficients[shape]

def calculate_trajectory_and_heating(probe: ProbeConfig, max_time: float = 1000, dt: float = 0.1):
    """Calculate trajectory and heating over time with shape-specific factors"""
    time_points = np.arange(0, max_time, dt)
    
    # Arrays for storing results
    altitudes = np.zeros_like(time_points)
    velocities = np.zeros_like(time_points)
    heat_fluxes = np.zeros_like(time_points)
    conv_heat_fluxes = np.zeros_like(time_points)
    heat_loads = np.zeros_like(time_points)
    pressures = np.zeros_like(time_points)
    temp_energy = np.zeros_like(time_points)
    # Initial conditions
    altitudes[0] = 300e3  # m (150 km)
    velocities[0] = probe.velocity
    
    # Get shape-specific coefficients
    shape_coeff = get_shape_coefficients(probe.shape)
    
    # Calculate reference area based on shape
    if probe.shape == 'sphere':
        area = np.pi * (probe.diameter/2)**2
    elif probe.shape == 'cube':
        area = probe.diameter**2  # face area
    elif probe.shape in ['cone', 'double_cone']:
        area = np.pi * (probe.diameter/2)**2
    
    entry_angle_rad = np.radians(probe.entry_angle)
    
    for i in range(1, len(time_points)):
        # Atmospheric properties using exponential model
        scale_height = 7400  # m
        rho = 1.225 * np.exp(-altitudes[i-1] / scale_height)  # kg/m³
        
        # Calculate convective heat flux (Sutton-Graves equation)
        k_sg = 1.7415e-4  # Sutton-Graves constant
        q_conv = k_sg * np.sqrt(rho/probe.diameter) * velocities[i-1]**3
        
        # Apply shape-specific heat factor
        q_conv *= shape_coeff['heat_factor']
        conv_heat_fluxes[i-1] = q_conv
        
        # Add radiative heating if velocity > 7.5 km/s
        if velocities[i-1] > 7500:
            C = 4.736e4
            q_rad = C * rho**1.22 * (velocities[i-1]/1e4)**3 * probe.diameter**0.5
            q_rad *= shape_coeff['pressure_coefficient']
        else:
            q_rad = 0
        
        # Total heat flux (W/m²)
        heat_fluxes[i-1] = q_conv + q_rad
        
        # Calculate heat load (J/m²)
        if i > 0:
            heat_loads[i] = heat_loads[i-1] + heat_fluxes[i-1] * dt
        
        # Calculate drag force
        dynamic_pressure = 0.5 * rho * velocities[i-1]**2
        drag_force = shape_coeff['drag'] * dynamic_pressure * area
        
        # Update trajectory
        drag_acc = -drag_force / (area * probe.diameter * 1000)  # Approximate mass using area and diameter
        gravity_acc = -9.81 * (6371000 / (6371000 + altitudes[i-1]))**2  # Variable gravity
        
        # Update velocity and position
        velocities[i] = velocities[i-1] + (drag_acc + gravity_acc * np.sin(entry_angle_rad)) * dt
        altitudes[i] = altitudes[i-1] + velocities[i-1] * np.sin(entry_angle_rad) * dt
        
        # Break if below surface or velocity too low
        if altitudes[i] < 0 or velocities[i] < 100:
            return {
                'times': time_points[:i],
                'altitudes': altitudes[:i],
                'velocities': velocities[:i],
                'heat_fluxes': heat_fluxes[:i],
                'conv_heat_fluxes': conv_heat_fluxes[:i],
                'heat_loads': heat_loads[:i]
            }
    
    return {
        'times': time_points,
        'altitudes': altitudes,
        'velocities': velocities,
        'heat_fluxes': heat_fluxes,
        'conv_heat_fluxes': conv_heat_fluxes,
        'heat_loads': heat_loads
    }

def plot_reentry_analysis():
    shapes = ['sphere', 'cube', 'cone', 'double_cone']
    diameter = 0.2  # 20 cm
    velocity = 8000  # 8 km/s
    
    fig = plt.figure(figsize=(15, 12))
    gs = fig.add_gridspec(3, 2)
    
    ax1 = fig.add_subplot(gs[0, 0])  # Heat Flux
    ax2 = fig.add_subplot(gs[0, 1])  # Convective Heat Flux
    ax3 = fig.add_subplot(gs[1, 0])  # Heat Load
    ax4 = fig.add_subplot(gs[1, 1])  # Velocity
    ax5 = fig.add_subplot(gs[2, :])  # Altitude
    
    colors = {'sphere': 'blue', 'cube': 'red', 'cone': 'green', 'double_cone': 'purple'}
    
    for shape in shapes:
        probe = ProbeConfig(shape, diameter, velocity)
        results = calculate_trajectory_and_heating(probe)
        
        style = {'color': colors[shape], 'label': shape.replace('_', ' ').title(), 'alpha': 0.8}
        
        # Convert heat flux to W/cm²
        ax1.plot(results['times'], results['heat_fluxes']/10000, **style)
        ax2.plot(results['times'], results['conv_heat_fluxes']/10000, **style)
        # Convert heat load to J/cm²
        ax3.plot(results['times'], results['heat_loads']/10000, **style)
        # Convert velocity to km/s
        ax4.plot(results['times'], results['velocities']/1000, **style)
        # Convert altitude to km
        ax5.plot(results['times'], results['altitudes']/1000, **style)
    
    # Configure plots
    ax1.set_ylabel('Total Heat Flux (W/cm²)')
    ax1.set_xlabel('Time (s)')
    ax1.set_title('Total Heat Flux vs Time')
    ax1.grid(True)
    ax1.legend()
    
    ax2.set_ylabel('Convective Heat Flux (W/cm²)')
    ax2.set_xlabel('Time (s)')
    ax2.set_title('Convective Heat Flux vs Time')
    ax2.grid(True)
    ax2.legend()
    
    ax3.set_ylabel('Heat Load (J/cm²)')
    ax3.set_xlabel('Time (s)')
    ax3.set_title('Heat Load vs Time')
    ax3.grid(True)
    ax3.legend()
    
    ax4.set_ylabel('Velocity (km/s)')
    ax4.set_xlabel('Time (s)')
    ax4.set_title('Velocity vs Time')
    ax4.grid(True)
    ax4.legend()
    
    ax5.set_ylabel('Altitude (km)')
    ax5.set_xlabel('Time (s)')
    ax5.set_title('Altitude vs Time')
    ax5.grid(True)
    ax5.legend()
    
    plt.tight_layout()
    return plt

# Run analysis and create plots
plot = plot_reentry_analysis()
plot.show()