"""
Uncertainty Analysis - Chemical Engineering Project
Demonstrates measurement uncertainty calculation and analysis
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd


class UncertaintyAnalyzer:
    """Class for performing uncertainty analysis in calibration"""
    
    def __init__(self):
        self.uncertainty_components = {}
        self.total_uncertainty = None
        
    def type_a_uncertainty(self, measurements):
        """Calculate Type A uncertainty (statistical analysis)"""
        n = len(measurements)
        mean = np.mean(measurements)
        std_dev = np.std(measurements, ddof=1)
        std_error = std_dev / np.sqrt(n)
        
        # 95% confidence interval
        t_value = stats.t.ppf(0.975, n - 1)
        confidence_interval = t_value * std_error
        
        results = {
            'mean': mean,
            'std_dev': std_dev,
            'std_error': std_error,
            'n_measurements': n,
            'degrees_of_freedom': n - 1,
            't_value': t_value,
            'confidence_interval': confidence_interval,
            'relative_std_error': (std_error / mean) * 100
        }
        
        self.uncertainty_components['type_a'] = results
        return results
    
    def type_b_uncertainty(self, tolerance, distribution='rectangular'):
        """Calculate Type B uncertainty (non-statistical)"""
        if distribution == 'rectangular':
            # Rectangular/uniform distribution
            uncertainty = tolerance / np.sqrt(3)
        elif distribution == 'triangular':
            # Triangular distribution
            uncertainty = tolerance / np.sqrt(6)
        elif distribution == 'normal':
            # Normal distribution (tolerance = 2*std_dev)
            uncertainty = tolerance / 2
        else:
            raise ValueError(f"Unknown distribution: {distribution}")
        
        results = {
            'tolerance': tolerance,
            'distribution': distribution,
            'uncertainty': uncertainty,
            'relative_uncertainty': (uncertainty / tolerance) * 100
        }
        
        self.uncertainty_components['type_b'] = results
        return results
    
    def combined_uncertainty(self, type_a_results, type_b_results):
        """Calculate combined standard uncertainty"""
        u_a = type_a_results['std_error']
        u_b = type_b_results['uncertainty']
        
        # Combined uncertainty (root sum of squares)
        u_c = np.sqrt(u_a**2 + u_b**2)
        
        # Effective degrees of freedom (Welch-Satterthwaite formula)
        v_a = type_a_results['degrees_of_freedom']
        v_b = np.inf  # Type B has infinite degrees of freedom
        
        if u_a > 0 and u_b > 0:
            v_eff = (u_c**4) / ((u_a**4 / v_a) + (u_b**4 / v_b))
        else:
            v_eff = v_a
        
        results = {
            'combined_uncertainty': u_c,
            'effective_dof': v_eff,
            'type_a_contribution': (u_a / u_c) * 100,
            'type_b_contribution': (u_b / u_c) * 100
        }
        
        self.total_uncertainty = results
        return results
    
    def expanded_uncertainty(self, combined_results, confidence_level=0.95):
        """Calculate expanded uncertainty"""
        v_eff = combined_results['effective_dof']
        u_c = combined_results['combined_uncertainty']
        
        # Coverage factor
        if v_eff >= 30:
            # Use normal distribution for large DOF
            k = stats.norm.ppf((1 + confidence_level) / 2)
        else:
            # Use t-distribution for small DOF
            k = stats.t.ppf((1 + confidence_level) / 2, v_eff)
        
        # Expanded uncertainty
        U = k * u_c
        
        results = {
            'expanded_uncertainty': U,
            'coverage_factor': k,
            'confidence_level': confidence_level,
            'effective_dof': v_eff,
            'relative_expanded_uncertainty': (U / u_c) * 100
        }
        
        return results
    
    def sensitivity_coefficient(self, nominal_value, variation):
        """Calculate sensitivity coefficient for a variable"""
        return variation / nominal_value
    
    def monte_carlo_uncertainty(self, function, distributions, n_simulations=10000):
        """Perform Monte Carlo uncertainty analysis"""
        results = []
        
        for _ in range(n_simulations):
            # Generate random values for each distribution
            values = {}
            for name, dist_params in distributions.items():
                dist_type = dist_params['type']
                if dist_type == 'normal':
                    values[name] = np.random.normal(dist_params['mean'], dist_params['std'])
                elif dist_type == 'uniform':
                    values[name] = np.random.uniform(dist_params['low'], dist_params['high'])
                elif dist_type == 'triangular':
                    values[name] = np.random.triangular(dist_params['left'], 
                                                       dist_params['mode'], 
                                                       dist_params['right'])
            
            # Evaluate function
            result = function(values)
            results.append(result)
        
        results = np.array(results)
        
        mc_results = {
            'mean': np.mean(results),
            'std_dev': np.std(results),
            'percentile_2.5': np.percentile(results, 2.5),
            'percentile_97.5': np.percentile(results, 97.5),
            'histogram': results
        }
        
        return mc_results
    
    def plot_uncertainty_distribution(self, measurements, title="Measurement Distribution"):
        """Plot histogram of measurements with uncertainty bands"""
        plt.figure(figsize=(10, 6))
        
        # Plot histogram
        plt.hist(measurements, bins=20, density=True, alpha=0.7, color='skyblue', 
                edgecolor='black', label='Measurements')
        
        # Calculate statistics
        mean = np.mean(measurements)
        std = np.std(measurements)
        
        # Plot normal distribution curve
        x = np.linspace(mean - 4*std, mean + 4*std, 100)
        plt.plot(x, stats.norm.pdf(x, mean, std), 'r-', linewidth=2, 
                label=f'Normal Distribution (μ={mean:.3f}, σ={std:.3f})')
        
        # Add uncertainty bands
        plt.axvline(mean - 2*std, color='orange', linestyle='--', 
                   label=f'±2σ ({2*std:.4f})')
        plt.axvline(mean + 2*std, color='orange', linestyle='--')
        
        plt.xlabel('Measurement Value')
        plt.ylabel('Probability Density')
        plt.title(title)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('uncertainty_distribution.png', dpi=150)
        plt.show()


def main():
    """Main function to demonstrate uncertainty analysis"""
    print("=" * 60)
    print("Uncertainty Analysis - Chemical Engineering Project")
    print("=" * 60)
    
    # Create analyzer instance
    analyzer = UncertaintyAnalyzer()
    
    # Example: pH meter calibration uncertainty
    print("\n1. pH Meter Calibration Uncertainty Analysis")
    print("-" * 60)
    
    # Type A uncertainty - repeated measurements
    ph_measurements = np.array([7.01, 6.99, 7.02, 7.00, 6.98, 7.01, 7.00, 6.99, 7.02, 7.00])
    
    print("\nType A Uncertainty (Statistical Analysis):")
    type_a = analyzer.type_a_uncertainty(ph_measurements)
    print(f"  Mean: {type_a['mean']:.4f} pH")
    print(f"  Standard Deviation: {type_a['std_dev']:.4f} pH")
    print(f"  Standard Error: {type_a['std_error']:.4f} pH")
    print(f"  95% Confidence Interval: ±{type_a['confidence_interval']:.4f} pH")
    print(f"  Relative Standard Error: {type_a['relative_std_error']:.2f}%")
    
    # Type B uncertainty - instrument specifications
    print("\nType B Uncertainty (Instrument Specifications):")
    type_b = analyzer.type_b_uncertainty(tolerance=0.05, distribution='rectangular')
    print(f"  Tolerance: ±{type_b['tolerance']:.3f} pH")
    print(f"  Distribution: {type_b['distribution']}")
    print(f"  Uncertainty: {type_b['uncertainty']:.4f} pH")
    print(f"  Relative Uncertainty: {type_b['relative_uncertainty']:.2f}%")
    
    # Combined uncertainty
    print("\nCombined Uncertainty:")
    combined = analyzer.combined_uncertainty(type_a, type_b)
    print(f"  Combined Uncertainty: {combined['combined_uncertainty']:.4f} pH")
    print(f"  Effective DOF: {combined['effective_dof']:.1f}")
    print(f"  Type A Contribution: {combined['type_a_contribution']:.1f}%")
    print(f"  Type B Contribution: {combined['type_b_contribution']:.1f}%")
    
    # Expanded uncertainty
    print("\nExpanded Uncertainty (95% confidence):")
    expanded = analyzer.expanded_uncertainty(combined, confidence_level=0.95)
    print(f"  Expanded Uncertainty: ±{expanded['expanded_uncertainty']:.4f} pH")
    print(f"  Coverage Factor (k): {expanded['coverage_factor']:.3f}")
    print(f"  Confidence Level: {expanded['confidence_level']*100:.0f}%")
    print(f"  Relative Expanded Uncertainty: {expanded['relative_expanded_uncertainty']:.2f}%")
    
    # Final result
    print("\n" + "=" * 60)
    print("FINAL RESULT:")
    print(f"  pH = {type_a['mean']:.3f} ± {expanded['expanded_uncertainty']:.3f} pH")
    print(f"  (k = {expanded['coverage_factor']:.3f}, p = {expanded['confidence_level']*100:.0f}%)")
    print("=" * 60)
    
    # Example 2: Concentration measurement uncertainty
    print("\n\n2. Concentration Measurement Uncertainty Analysis")
    print("-" * 60)
    
    # Simulated concentration measurements
    concentration_measurements = np.array([100.2, 99.8, 100.1, 100.3, 99.9, 
                                         100.0, 100.2, 99.7, 100.1, 100.0])
    
    print("\nType A Uncertainty:")
    type_a_conc = analyzer.type_a_uncertainty(concentration_measurements)
    print(f"  Mean: {type_a_conc['mean']:.3f} mg/L")
    print(f"  Standard Deviation: {type_a_conc['std_dev']:.3f} mg/L")
    print(f"  Standard Error: {type_a_conc['std_error']:.3f} mg/L")
    
    # Type B uncertainty - balance and volumetric flask
    print("\nType B Uncertainty Components:")
    
    # Balance uncertainty (rectangular distribution)
    balance_unc = analyzer.type_b_uncertainty(tolerance=0.001, distribution='rectangular')
    print(f"  Balance: {balance_unc['uncertainty']:.6f} mg")
    
    # Volumetric flask uncertainty (triangular distribution)
    flask_unc = analyzer.type_b_uncertainty(tolerance=0.05, distribution='triangular')
    print(f"  Volumetric Flask: {flask_unc['uncertainty']:.4f} mL")
    
    # Combined uncertainty
    type_b_combined = {
        'tolerance': np.sqrt(balance_unc['tolerance']**2 + flask_unc['tolerance']**2),
        'uncertainty': np.sqrt(balance_unc['uncertainty']**2 + flask_unc['uncertainty']**2),
        'distribution': 'combined'
    }
    
    combined_conc = analyzer.combined_uncertainty(type_a_conc, type_b_combined)
    expanded_conc = analyzer.expanded_uncertainty(combined_conc)
    
    print(f"\nCombined Uncertainty: {combined_conc['combined_uncertainty']:.4f} mg/L")
    print(f"Expanded Uncertainty: ±{expanded_conc['expanded_uncertainty']:.4f} mg/L")
    
    # Plot distribution
    print("\nPlotting uncertainty distribution...")
    analyzer.plot_uncertainty_distribution(concentration_measurements, 
                                         "Concentration Measurement Distribution")
    
    # Monte Carlo example
    print("\n\n3. Monte Carlo Uncertainty Propagation Example")
    print("-" * 60)
    
    def concentration_function(values):
        """Function to calculate concentration: C = m / V"""
        return values['mass'] / values['volume']
    
    # Define distributions
    distributions = {
        'mass': {
            'type': 'normal',
            'mean': 1.000,  # grams
            'std': 0.001    # grams
        },
        'volume': {
            'type': 'uniform',
            'low': 0.999,   # liters
            'high': 1.001   # liters
        }
    }
    
    mc_results = analyzer.monte_carlo_uncertainty(concentration_function, distributions)
    
    print(f"Monte Carlo Results (10,000 simulations):")
    print(f"  Mean Concentration: {mc_results['mean']:.4f} g/L")
    print(f"  Standard Deviation: {mc_results['std_dev']:.4f} g/L")
    print(f"  95% CI: [{mc_results['percentile_2.5']:.4f}, {mc_results['percentile_97.5']:.4f}] g/L")
    
    # Plot Monte Carlo results
    plt.figure(figsize=(10, 6))
    plt.hist(mc_results['histogram'], bins=50, density=True, alpha=0.7, 
            color='lightgreen', edgecolor='black')
    plt.axvline(mc_results['percentile_2.5'], color='red', linestyle='--', 
               label=f"2.5%: {mc_results['percentile_2.5']:.4f}")
    plt.axvline(mc_results['percentile_97.5'], color='red', linestyle='--', 
               label=f"97.5%: {mc_results['percentile_97.5']:.4f}")
    plt.xlabel('Concentration (g/L)')
    plt.ylabel('Probability Density')
    plt.title('Monte Carlo Uncertainty Propagation')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('monte_carlo_results.png', dpi=150)
    plt.show()
    
    print("\n" + "=" * 60)
    print("Uncertainty analysis completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
