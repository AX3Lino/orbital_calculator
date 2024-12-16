import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from nrlmsis_calculator import get_atmospheric_data as nrlmsis



class Shape:
    def __init__(self, name, volume, profile=None):
        """
        Initialize the shape with necessary parameters.

        Parameters:
            name (str): The name of the shape ('sphere', 'cube', or 'double_cone').
            volume (float): Volume of the shape in cubic meters.
            velocity (float): Velocity in m/s.
            density (float): Air density in kg/m³.
            profile (float, optional): profile along the body for heat flux calculation (0 to 1).
        """
        self.name = name
        self.volume = volume
        self.profile = profile
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

    def calculate_drag_force(self, density, velocity, temperature):
        """Calculate drag force based on shape and velocity."""
        gamma=1.4
        R = 287
        mach=np.sqrt(gamma * R * temperature)
        mach_number=velocity/mach
        if self.name == 'sphere':
            c = 0.47 if mach_number < 1 else 0.92
        elif self.name == 'cube':
            c = 1.05 if mach_number < 1 else 1.5
        elif self.name == 'double_cone':
            c = 0.5 if mach_number < 1 else 0.8
        else:
            raise ValueError(f"Unknown shape: {self.name}")

        return 0.5 * density * c * self.reference_area * velocity**2


    def calculate_heat_flux_coefficient(self,density,velocity):
        """Calculate heat flux coefficient using Sutton-Graves equation."""
        k = 1.742e-4  # Sutton-Graves constant
        return k * np.sqrt(density / self.characteristic_length) * velocity**3

    def calculate_distributed_heat_flux(self, density, velocity):
        """
        Calculate heat flux distributed along the body.

        Parameters:
            density (float): Air density in kg/m³.
            velocity (float): Velocity in m/s.

        Returns:
            float: Heat flux at the specified profile.
        """
        if self.profile is None:
            return self.calculate_heat_flux_coefficient(density,velocity)

        nose_heat_flux = self.calculate_heat_flux_coefficient(density,velocity)
        if self.name == 'sphere':
            theta = self.profile * np.pi
            return nose_heat_flux * np.cos(theta/2)**2
        elif self.name == 'cube':
            return nose_heat_flux * (1 - self.profile)
        elif self.name == 'double_cone':
            return nose_heat_flux * np.exp(-2 * self.profile)
        else:
            raise ValueError(f"Unknown shape: {self.name}")



if __name__ == "__main__":
    # Example usage
    temp,den=nrlmsis(0, 120, 0, 0)
    print(temp, den)
    shapes = [
        {"name": "sphere", "volume": 0.001,},
        {"name": "cube", "volume": 0.001,},
        {"name": "double_cone", "volume": 0.001,},
    ]
    velocity=7000
    for shape_data in shapes:
        shape = Shape(**shape_data)
        print(f"Shape: {shape.name}")
        print(f"  Characteristic Length: {shape.characteristic_length:.4f} m")
        print(f"  Reference Area: {shape.reference_area:.4f} m²")
        print(f"  Drag Coefficient: {shape.calculate_drag_force(den, velocity, temp):.4f}")
        print(f"  Heat Flux Coefficient: {shape.calculate_heat_flux_coefficient(den,velocity):.4e} W/m²")
        print(f"  Distributed Heat Flux (profile=0.5): {shape.calculate_distributed_heat_flux(den,velocity):.4e} W/m²")
        print()


    # Create a figure for the plot
    plt.figure(figsize=(10, 6))

    # Loop over each shape
    for shape_data in shapes:
        # Create a Shape instance
        shape = Shape(**shape_data)
        
        # Calculate distributed heat flux across normalized profiles
        profiles = np.linspace(0, 1, 100)
        heat_flux = [Shape(**shape_data, profile=pos).calculate_distributed_heat_flux(den,velocity) for pos in profiles]
        
        # Plot the results
        plt.plot(profiles, heat_flux, label=shape.name.capitalize())

    # Customize the plot
    plt.title("Distributed Heat Flux for Different Shapes", fontsize=16, fontweight="bold")
    plt.xlabel("Normalized profile", fontsize=14)
    plt.ylabel("Heat Flux (W/m²)", fontsize=14)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=12)
    plt.tight_layout()

    # Show the plot
    plt.show()

