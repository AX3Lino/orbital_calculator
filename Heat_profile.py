import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from nrlmsis_calculator import get_atmospheric_data as nrlmsis
class Shape:
    def __init__(self, name, volume, velocity, density, position=None):
        """
        Initialize the shape with necessary parameters.

        Parameters:
            name (str): The name of the shape ('sphere', 'cube', or 'double_cone').
            volume (float): Volume of the shape in cubic meters.
            velocity (float): Velocity in m/s.
            density (float): Air density in kg/m³.
            position (float, optional): Position along the body for heat flux calculation (0 to 1).
        """
        self.name = name
        self.volume = volume
        self.velocity = velocity
        self.density = density
        self.position = position
        self.characteristic_length = self._calculate_characteristic_length()
        self.reference_area = self._calculate_reference_area()

    def _calculate_characteristic_length(self):
        """Calculate characteristic length based on shape and volume."""
        if self.name == 'sphere':
            return 2 * (3 * self.volume / (4 * np.pi)) ** (1 / 3)  # Diameter
        elif self.name == 'cube':
            return self.volume ** (1 / 3)  # Side length
        elif self.name == 'double_cone':
            radius = (3 * self.volume / (2 * np.pi)) ** (1 / 3)
            return 4 * radius  # Total length
        else:
            raise ValueError(f"Unknown shape: {self.name}")

    def _calculate_reference_area(self):
        """Calculate reference area based on shape."""
        if self.name == 'sphere':
            radius = (3 * self.volume / (4 * np.pi)) ** (1 / 3)
            return np.pi * radius**2
        elif self.name == 'cube':
            side = self.volume ** (1 / 3)
            return side**2
        elif self.name == 'double_cone':
            radius = (3 * self.volume / (2 * np.pi)) ** (1 / 3)
            return np.pi * radius**2
        else:
            raise ValueError(f"Unknown shape: {self.name}")

    def calculate_drag_coefficient(self, mach_number):
        """Calculate drag coefficient based on shape and Mach number."""
        if self.name == 'sphere':
            return 0.47 if mach_number < 1 else 0.92
        elif self.name == 'cube':
            return 1.05 if mach_number < 1 else 1.5
        elif self.name == 'double_cone':
            return 0.5 if mach_number < 1 else 0.8
        else:
            raise ValueError(f"Unknown shape: {self.name}")

    def calculate_heat_flux_coefficient(self):
        """Calculate heat flux coefficient using Sutton-Graves equation."""
        k = 1.742e-4  # Sutton-Graves constant
        return k * np.sqrt(self.density / self.characteristic_length) * self.velocity**3

    def calculate_distributed_heat_flux(self):
        """
        Calculate heat flux distributed along the body.

        Returns:
            float: Heat flux at the specified position.
        """
        if self.position is None:
            return self.calculate_heat_flux_coefficient()

        nose_heat_flux = self.calculate_heat_flux_coefficient()
        if self.name == 'sphere':
            theta = self.position * np.pi
            return nose_heat_flux * np.cos(theta)
        elif self.name == 'cube':
            return nose_heat_flux * (1 - self.position)
        elif self.name == 'double_cone':
            return nose_heat_flux * np.exp(-2 * self.position)
        else:
            raise ValueError(f"Unknown shape: {self.name}")

# Example usage
den=nrlmsis(time, 120, 0, 0)[1]

shapes = [
    {"name": "sphere", "volume": 0.001, "velocity": 1000, "density": 0.02},
    {"name": "cube", "volume": 0.001, "velocity": 1000, "density": 0.02},
    {"name": "double_cone", "volume": 0.001, "velocity": 1000, "density": 0.02},
]


for shape_data in shapes:
    shape = Shape(**shape_data)
    mach_number = shape_data["velocity"] / 340  # Approximate Mach number
    print(f"Shape: {shape.name}")
    print(f"  Characteristic Length: {shape.characteristic_length:.4f} m")
    print(f"  Reference Area: {shape.reference_area:.4f} m²")
    print(f"  Drag Coefficient: {shape.calculate_drag_coefficient(mach_number):.4f}")
    print(f"  Heat Flux Coefficient: {shape.calculate_heat_flux_coefficient():.4e} W/m²")
    print(f"  Distributed Heat Flux (position=0.5): {shape.calculate_distributed_heat_flux():.4e} W/m²")
    print()


# Create a figure for the plot
plt.figure(figsize=(10, 6))

# Loop over each shape
for shape_data in shapes:
    # Create a Shape instance
    shape = Shape(**shape_data)
    
    # Calculate distributed heat flux across normalized positions
    positions = np.linspace(0, 1, 100)
    heat_flux = [Shape(**shape_data, position=pos).calculate_distributed_heat_flux() for pos in positions]
    
    # Plot the results
    plt.plot(positions, heat_flux, label=shape.name.capitalize())

# Customize the plot
plt.title("Distributed Heat Flux for Different Shapes", fontsize=16, fontweight="bold")
plt.xlabel("Normalized Position", fontsize=14)
plt.ylabel("Heat Flux (W/m²)", fontsize=14)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=12)
plt.tight_layout()

# Show the plot
plt.show()
