# Uncertainty Analysis Documentation

## Overview

Measurement uncertainty is a critical parameter in chemical engineering that quantifies the quality of measurement results. This document provides comprehensive guidance on uncertainty analysis principles, methods, and applications.

## 1. Introduction to Measurement Uncertainty

### What is Measurement Uncertainty?
- Parameter associated with the result of a measurement
- Characterizes the dispersion of values that could reasonably be attributed to the measurand
- Provides a quantitative estimate of measurement quality

### Why is Uncertainty Important?
- Ensures measurement reliability
- Supports decision-making
- Enables comparison of results
- Required by quality standards (ISO 9001, ISO/IEC 17025)
- Legal and regulatory requirements

## 2. Types of Uncertainty

### Type A Uncertainty (Statistical Analysis)
- Based on statistical analysis of a series of observations
- Calculated from repeated measurements
- Represents random errors
- Example: Standard deviation of 10 replicate measurements

**Calculation:**
```
Standard Deviation (s) = √[Σ(xᵢ - x̄)² / (n-1)]
Standard Error (uₐ) = s / √n
```

### Type B Uncertainty (Non-Statistical)
- Based on other means than statistical analysis
- Comes from calibration certificates, specifications, literature
- Represents systematic errors
- Example: Instrument tolerance, reference standard uncertainty

**Calculation:**
- Rectangular distribution: u = a / √3
- Triangular distribution: u = a / √6
- Normal distribution: u = a / 2 (where a = 2σ)

## 3. Uncertainty Budget Components

### Common Sources of Uncertainty in Chemical Engineering

#### Sampling Uncertainty
- Sample collection method
- Sample preparation
- Sample storage
- Sample representativeness

#### Instrument Uncertainty
- Resolution
- Accuracy specification
- Calibration uncertainty
- Drift over time

#### Method Uncertainty
- Repeatability
- Reproducibility
- Interferences
- Chemical reactions

#### Environmental Uncertainty
- Temperature effects
- Pressure effects
- Humidity
- Vibration

#### Operator Uncertainty
- Reading errors
- Timing errors
- Technique variations

## 4. Uncertainty Calculation Methods

### Step-by-Step Method

1. **Define the Measurand**
   - Clearly state what is being measured
   - Identify all input quantities

2. **Identify Uncertainty Sources**
   - List all potential sources
   - Use cause-and-effect diagrams (fishbone diagrams)

3. **Quantify Uncertainty Components**
   - Type A: Statistical analysis of data
   - Type B: Evaluate from certificates, specifications, etc.

4. **Calculate Combined Uncertainty**
   - Root sum of squares of all components
   - Include sensitivity coefficients

5. **Calculate Expanded Uncertainty**
   - Multiply combined uncertainty by coverage factor
   - State confidence level

### Mathematical Framework

#### Combined Standard Uncertainty
```
uₐ(y) = √[Σ(cᵢ² × u²(xᵢ))]
```
Where:
- cᵢ = sensitivity coefficient = ∂f/∂xᵢ
- u(xᵢ) = standard uncertainty of input quantity

#### Sensitivity Coefficients
```
cᵢ = ∂f/∂xᵢ
```
For linear functions: cᵢ = coefficient of xᵢ
For non-linear functions: evaluate partial derivative

#### Expanded Uncertainty
```
U = k × uₐ(y)
```
Where:
- k = coverage factor (typically 2 for 95% confidence)
- uₐ(y) = combined standard uncertainty

## 5. Degrees of Freedom

### What are Degrees of Freedom?
- Measure of the amount of information used to calculate uncertainty
- Higher DOF = more reliable uncertainty estimate
- Typically n-1 for statistical analysis

### Welch-Satterthwaite Formula
For combined uncertainty with different DOF components:
```
νeff = u⁴(c) / [Σ(uᵢ⁴ / νᵢ)]
```

### Coverage Factor Selection
- Large DOF (ν > 30): Use normal distribution (k = 1.96 for 95%)
- Small DOF: Use t-distribution
- k = t(ν, p) where p = confidence level

## 6. Practical Examples

### Example 1: Concentration Determination

**Problem:** Determine concentration and uncertainty for a solution prepared by:
- Weighing 1.000 g ± 0.001 g of solute
- Dissolving in 100.0 mL ± 0.1 mL volumetric flask

**Solution:**
```
C = m / V = 1.000 g / 0.1000 L = 10.00 g/L

Uncertainty components:
u(m) = 0.001 g / √3 = 0.00058 g (rectangular distribution)
u(V) = 0.1 mL / √6 = 0.041 mL (triangular distribution)

Sensitivity coefficients:
∂C/∂m = 1/V = 10 L⁻¹
∂C/∂V = -m/V² = -1000 g/L²

Combined uncertainty:
u(C) = √[(10 × 0.00058)² + (-1000 × 0.000041)²]
     = √[0.0000336 + 0.001681]
     = √0.001715 = 0.0414 g/L

Expanded uncertainty (95%, k=2):
U = 2 × 0.0414 = 0.083 g/L

Result: C = 10.00 ± 0.08 g/L
```

### Example 2: Titration Uncertainty

**Problem:** Determine NaOH concentration using HCl titration:
- HCl concentration: 0.1000 ± 0.0002 M
- Volume delivered: 25.00 ± 0.03 mL
- NaOH volume: 24.50 ± 0.02 mL

**Solution:**
```
C(NaOH) = C(HCl) × V(HCl) / V(NaOH)
         = 0.1000 × 25.00 / 24.50
         = 0.1020 M

Uncertainty components:
u(C_HCl) = 0.0002 / √3 = 0.000115 M
u(V_HCl) = 0.03 / √6 = 0.0122 mL
u(V_NaOH) = 0.02 / √6 = 0.00816 mL

Sensitivity coefficients:
∂C/∂C_HCl = V_HCl / V_NaOH = 1.020
∂C/∂V_HCl = C_HCl / V_NaOH = 0.00408 M/mL
∂C/∂V_NaOH = -C_HCl × V_HCl / V_NaOH² = -0.00417 M/mL

Combined uncertainty:
u(C) = √[(1.020 × 0.000115)² + (0.00408 × 0.0122)² + (-0.00417 × 0.00816)²]
     = √[1.38×10⁻⁸ + 2.50×10⁻⁹ + 1.15×10⁻⁹]
     = √1.75×10⁻⁸ = 0.000132 M

Expanded uncertainty (95%, k=2):
U = 2 × 0.000132 = 0.00026 M

Result: C(NaOH) = 0.1020 ± 0.0003 M
```

### Example 3: pH Measurement Uncertainty

**Problem:** pH meter reading 7.00 ± ?
- Meter specification: ±0.01 pH
- Buffer uncertainty: ±0.005 pH
- Temperature effect: ±0.003 pH
- Repeatability: ±0.008 pH (from 10 measurements)

**Solution:**
```
Uncertainty components:
u(meter) = 0.01 / √3 = 0.0058 pH (rectangular)
u(buffer) = 0.005 / √6 = 0.0020 pH (triangular)
u(temp) = 0.003 / √3 = 0.0017 pH (rectangular)
u(repeatability) = 0.008 / √10 = 0.0025 pH (Type A)

Combined uncertainty:
u(pH) = √[0.0058² + 0.0020² + 0.0017² + 0.0025²]
      = √[3.36×10⁻⁵ + 4.00×10⁻⁶ + 2.89×10⁻⁶ + 6.25×10⁻⁶]
      = √4.67×10⁻⁵ = 0.0068 pH

Expanded uncertainty (95%, k=2):
U = 2 × 0.0068 = 0.014 pH

Result: pH = 7.00 ± 0.01 pH
```

## 7. Uncertainty in Calibration

### Calibration Curve Uncertainty
- Uncertainty in slope and intercept
- Uncertainty in predicted values
- Confidence bands on calibration curve

### Propagation Through Calibration
For y = mx + b:
```
u(y) = √[(x × u(m))² + (m × u(x))² + (u(b))²]
```

### Limit of Detection Uncertainty
```
LOD = 3.3 × u(baseline) / slope
```

## 8. Reporting Uncertainty

### What to Report
- Measured value with units
- Expanded uncertainty with units
- Coverage factor (k)
- Confidence level (p)
- Degrees of freedom (if < 30)

### Report Format Examples
```
Result = (10.00 ± 0.08) g/L (k = 2, p = 95%)
Result = 7.00 ± 0.01 pH (k = 2, 95% confidence)
Result = 0.1020 ± 0.0003 M (νeff = 25, p = 95%)
```

### Uncertainty Statement Guidelines
- Report only significant figures
- Usually 1-2 significant figures for uncertainty
- Round up to be conservative
- Match precision of result to uncertainty

## 9. Monte Carlo Method

### When to Use Monte Carlo
- Complex non-linear functions
- Non-normal distributions
- Correlated input quantities
- When analytical methods are impractical

### Procedure
1. Define probability distributions for all inputs
2. Generate random values from each distribution
3. Propagate through model function
4. Analyze output distribution
5. Determine mean and confidence intervals

### Advantages
- Handles any distribution shape
- No linearization required
- Provides full output distribution
- Easy to implement with computers

## 10. Quality Assurance of Uncertainty Estimates

### Verification Methods
- Compare with historical data
- Check against independent measurements
- Use control charts
- Participate in proficiency testing

### Common Errors to Avoid
- Ignoring correlation between inputs
- Forgetting sensitivity coefficients
- Using wrong distribution type
- Underestimating Type B components
- Not updating uncertainty with new data

## 11. Software Tools

### Recommended Software
- **GUM Workbench** - Dedicated uncertainty calculation
- **MATLAB** - Statistical analysis and Monte Carlo
- **Python** - NumPy, SciPy, uncertainty libraries
- **Excel** - Basic uncertainty calculations
- **NIST Uncertainty Machine** - Online tool

### Python Libraries
- `uncertainty` - Uncertainty propagation
- `lmfit` - Curve fitting with uncertainty
- `scipy.stats` - Statistical distributions
- `numpy` - Numerical calculations

## 12. References

1. GUM: Guide to the Expression of Uncertainty in Measurement (ISO)
2. JCGM 100:2008 - Evaluation of measurement data
3. Eurachem/CITAC Guide CG 4 - Quantifying uncertainty in analytical measurement
4. NIST Technical Note 1297 - Guidelines for evaluating and expressing uncertainty
5. UKAS M3003 - The Expression of Uncertainty and Confidence in Measurement

## Appendix A: Common Distributions

| Distribution | Formula | Use Case |
|-------------|---------|----------|
| Rectangular | u = a/√3 | Digital display, tolerances |
| Triangular | u = a/√6 | Weighting, small samples |
| Normal | u = σ | Repeated measurements |
| U-shaped | u = a/√2 | Phase effects |

## Appendix B: Coverage Factors

| νeff | k (95%) | k (99%) |
|------|---------|---------|
| 1 | 12.71 | 63.66 |
| 2 | 4.30 | 9.92 |
| 5 | 2.57 | 4.03 |
| 10 | 2.23 | 3.17 |
| 20 | 2.09 | 2.85 |
| 30 | 2.04 | 2.75 |
| ∞ | 1.96 | 2.58 |
