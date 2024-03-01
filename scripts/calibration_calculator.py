"""
Calibration Calculator - Chemical Engineering Project
Demonstrates calibration curve generation and instrument validation
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd


class CalibrationCalculator:
    """Main class for calibration calculations and analysis"""
    
    def __init__(self):
        self.calibration_data = None
        self.calibration_curve = None
        self.r_squared = None
        
    def load_calibration_data(self, file_path):
        """Load calibration data from CSV file"""
        try:
            self.calibration_data = pd.read_csv(file_path)
            print(f"Loaded {len(self.calibration_data)} data points")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def generate_calibration_curve(self, x_col, y_col):
        """Generate linear calibration curve from data"""
        if self.calibration_data is None:
            print("No calibration data loaded")
            return None
        
        x = self.calibration_data[x_col].values
        y = self.calibration_data[y_col].values
        
        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        self.calibration_curve = {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_value**2,
            'std_error': std_err,
            'p_value': p_value
        }
        
        self.r_squared = r_value**2
        
        return self.calibration_curve
    
    def calculate_uncertainty(self, x, y, confidence_level=0.95):
        """Calculate calibration uncertainty"""
        if self.calibration_curve is None:
            print("No calibration curve generated")
            return None
        
        n = len(x)
        x_mean = np.mean(x)
        
        # Standard error of estimate
        y_pred = self.calibration_curve['slope'] * x + self.calibration_curve['intercept']
        residuals = y - y_pred
        se = np.sqrt(np.sum(residuals**2) / (n - 2))
        
        # Confidence interval
        t_value = stats.t.ppf((1 + confidence_level) / 2, n - 2)
        uncertainty = t_value * se * np.sqrt(1 + 1/n + (x - x_mean)**2 / np.sum((x - x_mean)**2))
        
        return uncertainty
    
    def plot_calibration_curve(self, x_col, y_col, title="Calibration Curve"):
        """Plot calibration curve with data points"""
        if self.calibration_data is None or self.calibration_curve is None:
            print("No data or calibration curve available")
            return
        
        x = self.calibration_data[x_col].values
        y = self.calibration_data[y_col].values
        
        # Generate fitted line
        x_fit = np.linspace(min(x), max(x), 100)
        y_fit = self.calibration_curve['slope'] * x_fit + self.calibration_curve['intercept']
        
        # Calculate uncertainty
        uncertainty = self.calculate_uncertainty(x, y)
        
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, label='Calibration Points', color='blue', alpha=0.6)
        plt.plot(x_fit, y_fit, 'r-', label=f'Linear Fit (R²={self.r_squared:.4f})')
        plt.fill_between(x_fit, y_fit - uncertainty, y_fit + uncertainty, 
                         alpha=0.2, color='red', label='95% Confidence Interval')
        
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(title)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('calibration_curve.png', dpi=150)
        plt.show()
        
    def validate_calibration(self, acceptance_criteria):
        """Validate calibration against acceptance criteria"""
        if self.calibration_curve is None:
            print("No calibration curve to validate")
            return False
        
        validation_results = {
            'r_squared_check': self.r_squared >= acceptance_criteria.get('min_r_squared', 0.99),
            'slope_check': abs(self.calibration_curve['slope'] - 1.0) <= acceptance_criteria.get('slope_tolerance', 0.1),
            'intercept_check': abs(self.calibration_curve['intercept']) <= acceptance_criteria.get('intercept_tolerance', 0.01)
        }
        
        all_passed = all(validation_results.values())
        
        print("\nCalibration Validation Results:")
        print("-" * 40)
        for check, result in validation_results.items():
            status = "PASS" if result else "FAIL"
            print(f"{check}: {status}")
        print("-" * 40)
        print(f"Overall: {'PASS' if all_passed else 'FAIL'}")
        
        return all_passed


def main():
    """Main function to demonstrate calibration calculator"""
    print("=" * 50)
    print("Calibration Engineering Project")
    print("Chemical Engineering Demonstration")
    print("=" * 50)
    
    # Create calculator instance
    calculator = CalibrationCalculator()
    
    # Example: Generate sample calibration data
    np.random.seed(42)
    concentrations = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    absorbance = 0.02 * concentrations + 0.1 + np.random.normal(0, 0.05, len(concentrations))
    
    # Create sample data frame
    sample_data = pd.DataFrame({
        'Concentration (mg/L)': concentrations,
        'Absorbance': absorbance
    })
    
    # Save sample data
    sample_data.to_csv('sample_calibration_data.csv', index=False)
    print("\nSample calibration data generated")
    
    # Load data
    calculator.calibration_data = sample_data
    
    # Generate calibration curve
    print("\nGenerating calibration curve...")
    curve = calculator.generate_calibration_curve('Concentration (mg/L)', 'Absorbance')
    
    if curve:
        print(f"\nCalibration Results:")
        print(f"Slope: {curve['slope']:.6f}")
        print(f"Intercept: {curve['intercept']:.6f}")
        print(f"R-squared: {curve['r_squared']:.6f}")
        print(f"Standard Error: {curve['std_error']:.6f}")
    
    # Validate calibration
    acceptance_criteria = {
        'min_r_squared': 0.99,
        'slope_tolerance': 0.1,
        'intercept_tolerance': 0.01
    }
    
    calculator.validate_calibration(acceptance_criteria)
    
    # Plot calibration curve
    print("\nPlotting calibration curve...")
    calculator.plot_calibration_curve('Concentration (mg/L)', 'Absorbance')
    
    print("\n" + "=" * 50)
    print("Calibration project completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()
