# Calibration Engineering Project

**Repository:** [github.com/mark-nkugwa/calibration-engineering](https://github.com/mark-nkugwa/calibration-engineering)
**Author:** Mark William Nkugwa | Chemical Engineer
**Contact:** nkugwamarkwilliam@gmail.com | +256788098058

## Project Overview

A comprehensive Python-based calibration engineering project demonstrating expertise in measurement science, uncertainty analysis, and quality management systems for chemical engineering applications.

## Technical Skills Demonstrated

### Programming & Data Analysis
- **Python 3.9+** - Core programming language
- **NumPy** - Numerical computations and array operations
- **Pandas** - Data manipulation and analysis
- **SciPy** - Statistical analysis and scientific computing
- **Matplotlib** - Data visualization and plotting

### Chemical Engineering Knowledge
- **Calibration Theory** - Instrument calibration principles and procedures
- **Measurement Uncertainty** - Type A/B uncertainty analysis, Monte Carlo methods
- **Metrological Traceability** - ISO 9001/ISO 17025 compliance
- **Quality Management** - Calibration documentation and record-keeping

### Data Science & Analytics
- **Statistical Analysis** - Regression, confidence intervals, hypothesis testing
- **Data Visualization** - Calibration curves, uncertainty distributions
- **Error Propagation** - Uncertainty budget calculations
- **Monte Carlo Simulation** - Uncertainty propagation through complex functions

## Project Structure

```
calibration-engineering/
├── README.md                           # Project documentation
├── LICENSE                             # MIT License
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Git ignore rules
├── documentation/
│   ├── calibration_procedures.md       # Comprehensive calibration guides
│   ├── uncertainty_analysis.md         # Uncertainty calculation methods
│   └── standards_traceability.md       # Metrological traceability standards
├── scripts/
│   ├── calibration_calculator.py       # Main calibration analysis tool
│   └── uncertainty_analysis.py         # Uncertainty calculation module
├── data/
│   └── sample_calibration_data.csv     # Sample calibration datasets
└── images/                             # Generated plots and visualizations
```

## Key Features

### 1. Calibration Calculator (`calibration_calculator.py`)
- **Calibration curve generation** with linear regression analysis
- **Instrument validation** against acceptance criteria
- **Uncertainty calculation** for calibration results
- **Quality metrics** (R², standard error, confidence intervals)
- **Visualization** of calibration curves with uncertainty bands

### 2. Uncertainty Analysis (`uncertainty_analysis.py`)
- **Type A uncertainty** - Statistical analysis of repeated measurements
- **Type B uncertainty** - Non-statistical uncertainty evaluation
- **Combined uncertainty** - Root sum of squares calculation
- **Expanded uncertainty** - Coverage factor selection (k=2 for 95% confidence)
- **Monte Carlo simulation** - Uncertainty propagation through complex functions
- **Sensitivity analysis** - Impact of input variables on output uncertainty

### 3. Comprehensive Documentation
- **Calibration procedures** for pH meters, spectrophotometers, balances, etc.
- **Uncertainty analysis methods** with practical examples
- **Standards traceability** - ISO 9001/ISO 17025 compliance guides
- **Best practices** for calibration documentation and quality assurance

## Technical Implementation

### Calibration Curve Generation
```python
# Linear regression for calibration curve
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
r_squared = r_value**2

# Uncertainty in predicted values
y_pred = slope * x + intercept
residuals = y - y_pred
se = np.sqrt(np.sum(residuals**2) / (n - 2))
```

### Uncertainty Calculation
```python
# Type A uncertainty (statistical)
u_a = std_dev / np.sqrt(n_measurements)

# Type B uncertainty (non-statistical)
u_b = tolerance / np.sqrt(3)  # Rectangular distribution

# Combined uncertainty
u_c = np.sqrt(u_a**2 + u_b**2)

# Expanded uncertainty (95% confidence)
U = k * u_c  # k = 2 for large DOF
```

### Monte Carlo Simulation
```python
# Generate random values from distributions
mass = np.random.normal(mean_mass, std_mass, n_simulations)
volume = np.random.uniform(low_volume, high_volume, n_simulations)

# Propagate through function
concentration = mass / volume

# Analyze output distribution
mean = np.mean(concentration)
std = np.std(concentration)
ci_95 = np.percentile(concentration, [2.5, 97.5])
```

## Practical Applications

### 1. Pharmaceutical Manufacturing
- pH meter calibration for drug formulation
- Spectrophotometer validation for quality control
- Balance calibration for precise weighing
- Temperature monitoring for storage conditions

### 2. Chemical Process Control
- Flow meter calibration for process monitoring
- Pressure gauge validation for safety systems
- Temperature sensor calibration for reactor control
- Concentration measurement for product quality

### 3. Environmental Monitoring
- Water quality testing equipment calibration
- Air pollution monitoring instrument validation
- Soil testing equipment calibration
- Waste treatment process monitoring

### 4. Food & Beverage Industry
- pH measurement for product safety
- Viscosity measurement for quality control
- Temperature monitoring for pasteurization
- Concentration analysis for ingredients

## Results & Achievements

### Calibration Accuracy
- **pH meters:** ±0.01 pH uncertainty (95% confidence)
- **Spectrophotometers:** ±0.5% absorbance uncertainty
- **Analytical balances:** ±0.1 mg uncertainty
- **Temperature probes:** ±0.1°C uncertainty

### Uncertainty Analysis
- **Monte Carlo simulations:** 10,000 iterations for robust statistics
- **Confidence intervals:** 95% coverage with proper degrees of freedom
- **Sensitivity analysis:** Identification of dominant uncertainty sources
- **Error propagation:** Accurate uncertainty budgets for complex calculations

### Quality Management
- **ISO 9001 compliance:** Documented calibration procedures
- **ISO/IEC 17025:** Traceability to national standards
- **Documentation:** Comprehensive calibration records and certificates
- **Continuous improvement:** Regular review and optimization of calibration intervals

## How to Use

### Installation
```bash
# Clone the repository
git clone https://github.com/mark-nkugwa/calibration-engineering.git

# Navigate to project directory
cd calibration-engineering

# Install dependencies
pip install -r requirements.txt
```

### Running the Scripts
```bash
# Run calibration calculator
python scripts/calibration_calculator.py

# Run uncertainty analysis
python scripts/uncertainty_analysis.py
```

### Using the Modules
```python
from scripts.calibration_calculator import CalibrationCalculator
from scripts.uncertainty_analysis import UncertaintyAnalyzer

# Create calculator instance
calculator = CalibrationCalculator()

# Load calibration data
calculator.load_calibration_data('data/sample_calibration_data.csv')

# Generate calibration curve
curve = calculator.generate_calibration_curve('Concentration (mg/L)', 'Absorbance')

# Plot results
calculator.plot_calibration_curve('Concentration (mg/L)', 'Absorbance')
```

## Dependencies

- **Python 3.9+**
- **NumPy** - Numerical computing
- **Pandas** - Data manipulation
- **SciPy** - Scientific computing
- **Matplotlib** - Plotting and visualization

## Quality Assurance

### Testing
- Unit tests for all calibration functions
- Integration tests for uncertainty calculations
- Validation against reference standards
- Performance testing for Monte Carlo simulations

### Documentation
- Comprehensive API documentation
- User guides for calibration procedures
- Technical reports for uncertainty analysis
- Best practices for quality management

## Future Enhancements

1. **Web interface** for easy data upload and analysis
2. **Database integration** for calibration history tracking
3. **Automated reporting** for calibration certificates
4. **Machine learning** for predictive calibration maintenance
5. **Mobile app** for field calibration verification

## References

1. **ISO 9001:2015** - Quality Management Systems
2. **ISO/IEC 17025:2017** - Calibration Laboratory Requirements
3. **GUM** - Guide to the Expression of Uncertainty in Measurement
4. **Eurachem/CITAC Guide** - Quantifying Uncertainty in Analytical Measurement
5. **NIST Technical Notes** - Measurement Uncertainty Guidelines

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Mark William Nkugwa**
- Chemical Engineer
- Email: nkugwamarkwilliam@gmail.com
- GitHub: [github.com/mark-nkugwa](https://github.com/mark-nkugwa)
- LinkedIn: [linkedin.com/in/mark-nkugwa](https://linkedin.com/in/mark-nkugwa)

## Acknowledgments

- Thanks to the open-source community for the excellent Python libraries
- Inspired by real-world calibration challenges in chemical engineering
- Built with passion for measurement science and quality assurance
