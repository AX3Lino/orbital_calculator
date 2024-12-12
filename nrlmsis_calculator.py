from nrlmsise00 import gtd7_flat
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def get_atmospheric_data(time, height_km, lat_deg, lon_deg):
    """
    Get temperature and air density from the NRLMSISE-00 model.
    
    Parameters:
        time (datetime): Date and time (UTC).
        height_km (float): Altitude in kilometers.
        lat_deg (float): Latitude in degrees.
        lon_deg (float): Longitude in degrees.

    Returns:
        tuple: Temperature (K) and air density (kg/m³).
    """
    # Convert time to required inputs
    year = time.year-1 #last year 
    day_of_year = time.timetuple().tm_yday
    second_of_day = time.hour * 3600 + time.minute * 60 + time.second

    # Define inputs for the flattened gtd7 model
    inputs = {
        "alt": height_km,  # Altitude (km)
        "g_lat": lat_deg,  # Geographic latitude (deg)
        "g_long": lon_deg,  # Geographic longitude (deg)
        "year": year,
        "doy": day_of_year,  # Day of the year
        "sec": second_of_day,  # Seconds in the day
        "lst": lon_deg / 15.0,  # Local solar time (approx.)
        "f107A": 150.0,         # 3-month average solar flux
        "f107": 150.0,          # Daily solar flux
        "ap": 4                 # Geomagnetic activity index
    }

    # Run the model using the gtd7_flat interface
    result = gtd7_flat(**inputs)

    # Extract outputs (adjust indices based on documentation)
    density = result[5]  # Total mass density (kg/m³) (index 5)
    temperature = result[10]  # Exospheric temperature (K) (index 10)

    return temperature, density




if __name__ == "__main__":
    # Define the range of heights (in km) for which we want to get atmospheric data
    heights_km = np.linspace(0, 100, 101)  # Heights from 0 to 100 km
    
    # Define the time, latitude, and longitude for the data retrieval
    time = datetime.now()  # Example time (UTC)
    lat_deg = 0  # Example latitude (equator)
    lon_deg = 0  # Example longitude (prime meridian)

    # Initialize lists to store temperature and density data
    temperatures = []
    densities = []
    # Retrieve atmospheric data for each height
    for height_km in heights_km:
        temp, density = get_atmospheric_data(time, height_km, lat_deg, lon_deg)
        temperatures.append(temp)
        densities.append(density)
    # Convert lists to numpy arrays for plotting
    temperatures = np.array(temperatures)
    densities = np.array(densities)
    # Plot temperature vs. height
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(heights_km, temperatures, label='Temperature (K)')
    plt.xlabel('Height (km)')
    plt.ylabel('Temperature (K)')
    plt.title('Temperature vs. Height')
    plt.legend()

    # Plot density vs. height
    plt.subplot(1, 2, 2)
    plt.plot(heights_km, densities, label='Density (kg/m³)', color='orange')
    plt.yscale('log')
    plt.xlabel('Height (km)')
    plt.ylabel('Density (kg/m³)')
    plt.title('Density vs. Height')
    plt.legend()

    # Show the plots
    plt.tight_layout()
    plt .show()

