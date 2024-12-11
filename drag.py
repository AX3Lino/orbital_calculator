import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import os

class TemperatureDensityPredictor:
    def __init__(self, data_path, n_estimators=100, random_state=42):
        """
        Initialize the predictor by loading the data, preprocessing it, and training the models.

        Args:
            data_path (str): Path to the CSV file containing the data.
            n_estimators (int): Number of trees in the Random Forest model.
            random_state (int): Random seed for reproducibility.
        """
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file not found: {data_path}")
        
        # Load and preprocess data
        self.data = pd.read_csv(data_path)
        
        # Ensure required columns exist
        required_columns = {'height', 'latitude', 'longitude', 'temperature', 'density'}
        if not required_columns.issubset(self.data.columns):
            raise ValueError(f"Dataset must contain columns: {required_columns}")
        
        # Prepare features (X) and targets (y)
        X = self.data[['height', 'latitude', 'longitude']]
        y_temp = self.data['temperature']
        y_density = self.data['density']
        
        # Split data into training and testing sets
        X_train, X_test, y_temp_train, y_temp_test = train_test_split(
            X, y_temp, test_size=0.2, random_state=random_state
        )
        _, _, y_density_train, y_density_test = train_test_split(
            X, y_density, test_size=0.2, random_state=random_state
        )
        
        # Scale features
        self.scaler_X = StandardScaler()
        X_train_scaled = self.scaler_X.fit_transform(X_train)
        X_test_scaled = self.scaler_X.transform(X_test)
        
        # Train the models and calculate losses
        self.temp_model, self.temp_train_loss, self.temp_test_loss = self._train_and_evaluate(
            X_train_scaled, y_temp_train, X_test_scaled, y_temp_test, n_estimators, random_state
        )
        
        self.density_model, self.density_train_loss, self.density_test_loss = self._train_and_evaluate(
            X_train_scaled, y_density_train, X_test_scaled, y_density_test, n_estimators, random_state
        )
    
    def _train_and_evaluate(self, X_train, y_train, X_test, y_test, n_estimators, random_state):
        """
        Train a Random Forest model and calculate train and test losses.

        Args:
            X_train (ndarray): Scaled training feature matrix.
            y_train (ndarray): Training target values.
            X_test (ndarray): Scaled testing feature matrix.
            y_test (ndarray): Testing target values.
            n_estimators (int): Number of trees in the Random Forest model.
            random_state (int): Random seed for reproducibility.

        Returns:
            tuple: Trained model, training loss (float), testing loss (float).
        """
        model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
        model.fit(X_train, y_train)
        
        # Calculate losses
        train_loss = mean_squared_error(y_train, model.predict(X_train))
        test_loss = mean_squared_error(y_test, model.predict(X_test))
        
        return model, train_loss, test_loss
    
    def predict(self, height, latitude, longitude):
        """
        Predict temperature and density based on input parameters.

        Args:
            height (float): Height above sea level.
            latitude (float): Latitude in degrees.
            longitude (float): Longitude in degrees.

        Returns:
            tuple: Predicted temperature (float) and density (float).
        """
        # Prepare input features
        input_data = np.array([[height, latitude, longitude]])
        input_scaled = self.scaler_X.transform(input_data)
        
        # Predict temperature and density
        predicted_temp = self.temp_model.predict(input_scaled)[0]
        predicted_density = self.density_model.predict(input_scaled)[0]
        
        return predicted_temp, predicted_density
    
    def get_losses(self):
        """
        Get the training and testing losses for temperature and density models.

        Returns:
            dict: Dictionary containing train and test losses for both models.
        """
        return {
            "Temperature": {"Train Loss": self.temp_train_loss, "Test Loss": self.temp_test_loss},
            "Density": {"Train Loss": self.density_train_loss, "Test Loss": self.density_test_loss}
        }


def predict_temp_density(height, latitude, longitude, data_path='output.txt'):
    """
    Wrapper function to initialize the predictor and make predictions.

    Args:
        height (float): Height above sea level.
        latitude (float): Latitude in degrees.
        longitude (float): Longitude in degrees.
        data_path (str): Path to the CSV data file.

    Returns:
        tuple: Predicted temperature (float) and density (float).
    """
    predictor = TemperatureDensityPredictor(data_path)
    return predictor.predict(height, latitude, longitude)


# Example usage:
predictor = TemperatureDensityPredictor('output.txt')
temp, density = predictor.predict(1000, 40.7128, -74.0060)
losses = predictor.get_losses()
print(f"Temperature: {temp}°C, Air Density: {density} kg/m³")
print("Losses:", losses)
