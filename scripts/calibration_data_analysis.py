"""
Calibration Data Analysis - Chemical Engineering Project
Demonstrates advanced data analysis and statistical methods for calibration
"""

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class CalibrationDataAnalyzer:
    """Advanced calibration data analysis and statistical methods"""
    
    def __init__(self):
        self.data = None
        self.analysis_results = {}
        
    def load_calibration_data(self, file_path=None):
        """Load calibration data from CSV or create sample data"""
        if file_path and os.path.exists(file_path):
            self.data = pd.read_csv(file_path)
            print(f"Loaded data from {file_path}")
        else:
            # Create comprehensive sample calibration data
            np.random.seed(42)
            n_samples = 100
            
            data = {
                'sample_id': [f"SAMPLE-{i+1:04d}" for i in range(n_samples)],
                'concentration_mgL': np.concatenate([
                    np.random.uniform(0, 10, 20),
                    np.random.uniform(10, 50, 30),
                    np.random.uniform(50, 100, 30),
                    np.random.uniform(100, 200, 20)
                ]),
                'absorbance': np.concatenate([
                    np.random.normal(0.1, 0.02, 20),
                    np.random.normal(0.5, 0.03, 30),
                    np.random.normal(1.0, 0.04, 30),
                    np.random.normal(2.0, 0.05, 20)
                ]),
                'volume_mL': np.random.uniform(9.9, 10.1, n_samples),
                'mass_g': np.random.uniform(0.99, 1.01, n_samples),
                'temperature_C': np.random.normal(25, 0.5, n_samples),
                'pH': np.random.normal(7.0, 0.1, n_samples),
                'pressure_kPa': np.random.normal(101.3, 0.5, n_samples),
                'flow_rate_Lmin': np.random.uniform(0.9, 1.1, n_samples),
                'operator': np.random.choice(['Operator A', 'Operator B', 'Operator C'], n_samples),
                'instrument': np.random.choice(['Instrument 1', 'Instrument 2', 'Instrument 3'], n_samples),
                'date': pd.date_range(start='2024-01-01', periods=n_samples, freq='D')
            }
            
            self.data = pd.DataFrame(data)
            print("Sample calibration data created")
        
        return self.data
    
    def descriptive_statistics(self, columns=None):
        """Calculate descriptive statistics for calibration data"""
        if self.data is None:
            print("No data loaded")
            return None
        
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        stats_dict = {}
        for col in columns:
            if col in self.data.columns:
                col_data = self.data[col].dropna()
                stats_dict[col] = {
                    'count': len(col_data),
                    'mean': col_data.mean(),
                    'std': col_data.std(),
                    'min': col_data.min(),
                    'max': col_data.max(),
                    'range': col_data.max() - col_data.min(),
                    'median': col_data.median(),
                    'skewness': col_data.skew(),
                    'kurtosis': col_data.kurtosis(),
                    'cv': (col_data.std() / col_data.mean()) * 100  # Coefficient of variation
                }
        
        self.analysis_results['descriptive_statistics'] = stats_dict
        return stats_dict
    
    def correlation_analysis(self, x_col, y_col):
        """Perform correlation analysis between two variables"""
        if self.data is None:
            print("No data loaded")
            return None
        
        x = self.data[x_col].dropna()
        y = self.data[y_col].dropna()
        
        # Align data
        common_idx = x.index.intersection(y.index)
        x = x[common_idx]
        y = y[common_idx]
        
        # Calculate correlation
        correlation = x.corr(y)
        
        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Calculate residuals
        y_pred = slope * x + intercept
        residuals = y - y_pred
        
        results = {
            'correlation_coefficient': correlation,
            'r_squared': r_value**2,
            'slope': slope,
            'intercept': intercept,
            'std_error': std_err,
            'p_value': p_value,
            'residuals': residuals,
            'residual_std': residuals.std(),
            'residual_mean': residuals.mean()
        }
        
        self.analysis_results[f'correlation_{x_col}_{y_col}'] = results
        return results
    
    def outlier_detection(self, column, method='zscore', threshold=3):
        """Detect outliers in calibration data"""
        if self.data is None:
            print("No data loaded")
            return None
        
        data = self.data[column].dropna()
        
        if method == 'zscore':
            # Z-score method
            z_scores = np.abs(stats.zscore(data))
            outliers = data[z_scores > threshold]
            
        elif method == 'iqr':
            # IQR method
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            outliers = data[(data < lower_bound) | (data > upper_bound)]
            
        elif method == 'mad':
            # Median Absolute Deviation method
            median = data.median()
            mad = np.median(np.abs(data - median))
            modified_z_scores = 0.6745 * (data - median) / mad
            outliers = data[np.abs(modified_z_scores) > threshold]
            
        else:
            print(f"Unknown method: {method}")
            return None
        
        results = {
            'method': method,
            'threshold': threshold,
            'n_outliers': len(outliers),
            'outlier_indices': outliers.index.tolist(),
            'outlier_values': outliers.values.tolist(),
            'outlier_percentage': (len(outliers) / len(data)) * 100
        }
        
        self.analysis_results[f'outliers_{column}_{method}'] = results
        return results
    
    def normality_test(self, column):
        """Test if data follows normal distribution"""
        if self.data is None:
            print("No data loaded")
            return None
        
        data = self.data[column].dropna()
        
        # Shapiro-Wilk test
        shapiro_stat, shapiro_p = stats.shapiro(data)
        
        # D'Agostino-Pearson test
        dagostino_stat, dagostino_p = stats.normaltest(data)
        
        # Anderson-Darling test
        anderson_result = stats.anderson(data, dist='norm')
        
        # Kolmogorov-Smirnov test
        ks_stat, ks_p = stats.kstest(data, 'norm', args=(data.mean(), data.std()))
        
        results = {
            'shapiro_wilk': {'statistic': shapiro_stat, 'p_value': shapiro_p},
            'dagostino_pearson': {'statistic': dagostino_stat, 'p_value': dagostino_p},
            'anderson_darling': {
                'statistic': anderson_result.statistic,
                'critical_values': anderson_result.critical_values.tolist(),
                'significance_levels': anderson_result.significance_level.tolist()
            },
            'kolmogorov_smirnov': {'statistic': ks_stat, 'p_value': ks_p},
            'is_normal': shapiro_p > 0.05 and dagostino_p > 0.05
        }
        
        self.analysis_results[f'normality_{column}'] = results
        return results
    
    def anova_analysis(self, value_column, group_column):
        """Perform ANOVA analysis to compare groups"""
        if self.data is None:
            print("No data loaded")
            return None
        
        # Group data
        groups = []
        group_names = []
        
        for name, group in self.data.groupby(group_column):
            groups.append(group[value_column].dropna().values)
            group_names.append(name)
        
        # One-way ANOVA
        f_stat, p_value = stats.f_oneway(*groups)
        
        # Calculate group statistics
        group_stats = {}
        for name, group in self.data.groupby(group_column):
            data = group[value_column].dropna()
            group_stats[name] = {
                'count': len(data),
                'mean': data.mean(),
                'std': data.std(),
                'min': data.min(),
                'max': data.max()
            }
        
        results = {
            'f_statistic': f_stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'group_statistics': group_stats,
            'n_groups': len(groups)
        }
        
        self.analysis_results[f'anova_{value_column}_{group_column}'] = results
        return results
    
    def control_chart_analysis(self, column, subgroup_size=5):
        """Create control chart for process monitoring"""
        if self.data is None:
            print("No data loaded")
            return None
        
        data = self.data[column].dropna()
        
        # Calculate subgroup means and ranges
        n_subgroups = len(data) // subgroup_size
        subgroup_means = []
        subgroup_ranges = []
        
        for i in range(n_subgroups):
            start = i * subgroup_size
            end = start + subgroup_size
            subgroup = data.iloc[start:end]
            
            subgroup_means.append(subgroup.mean())
            subgroup_ranges.append(subgroup.max() - subgroup.min())
        
        subgroup_means = np.array(subgroup_means)
        subgroup_ranges = np.array(subgroup_ranges)
        
        # Calculate control limits
        x_bar = subgroup_means.mean()
        r_bar = subgroup_ranges.mean()
        
        # Control chart constants for subgroup size 5
        A2 = 0.577
        D3 = 0
        D4 = 2.114
        
        # X-bar chart limits
        UCL_x = x_bar + A2 * r_bar
        LCL_x = x_bar - A2 * r_bar
        
        # R chart limits
        UCL_r = D4 * r_bar
        LCL_r = D3 * r_bar
        
        # Check for out-of-control points
        out_of_control_x = np.where((subgroup_means > UCL_x) | (subgroup_means < LCL_x))[0]
        out_of_control_r = np.where(subgroup_ranges > UCL_r)[0]
        
        results = {
            'subgroup_means': subgroup_means.tolist(),
            'subgroup_ranges': subgroup_ranges.tolist(),
            'x_bar': x_bar,
            'r_bar': r_bar,
            'UCL_x': UCL_x,
            'LCL_x': LCL_x,
            'UCL_r': UCL_r,
            'LCL_r': LCL_r,
            'out_of_control_x': out_of_control_x.tolist(),
            'out_of_control_r': out_of_control_r.tolist(),
            'process_in_control': len(out_of_control_x) == 0 and len(out_of_control_r) == 0
        }
        
        self.analysis_results[f'control_chart_{column}'] = results
        return results
    
    def measurement_system_analysis(self, data_columns, operator_column):
        """Perform Measurement System Analysis (MSA)"""
        if self.data is None:
            print("No data loaded")
            return None
        
        # Prepare data for Gage R&R analysis
        operators = self.data[operator_column].unique()
        parts = self.data['sample_id'].unique()[:10]  # Use first 10 parts
        
        # Calculate variance components
        operator_means = {}
        part_means = {}
        interaction_var = 0
        
        for op in operators:
            op_data = self.data[self.data[operator_column] == op]
            operator_means[op] = op_data[data_columns].mean().mean()
        
        for part in parts:
            part_data = self.data[self.data['sample_id'] == part]
            part_means[part] = part_data[data_columns].mean().mean()
        
        # Calculate variance components (simplified)
        operator_var = np.var(list(operator_means.values()))
        part_var = np.var(list(part_means.values()))
        
        # Total variance
        total_var = self.data[data_columns].var().mean()
        
        # % Contribution
        %_operator = (operator_var / total_var) * 100 if total_var > 0 else 0
        %_part = (part_var / total_var) * 100 if total_var > 0 else 0
        %_grr = 100 - %_operator - %_part
        
        results = {
            'operator_variance': operator_var,
            'part_variance': part_var,
            'total_variance': total_var,
            'percent_operator': %_operator,
            'percent_part': %_part,
            'percent_gage_rr': %_grr,
            'measurement_system_acceptable': %_grr < 30,
            'operator_means': operator_means,
            'part_means': part_means
        }
        
        self.analysis_results['measurement_system_analysis'] = results
        return results
    
    def plot_calibration_curve(self, x_col, y_col, title="Calibration Curve"):
        """Plot calibration curve with analysis"""
        if self.data is None:
            print("No data loaded")
            return
        
        x = self.data[x_col].dropna()
        y = self.data[y_col].dropna()
        
        # Align data
        common_idx = x.index.intersection(y.index)
        x = x[common_idx]
        y = y[common_idx]
        
        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Generate fitted line
        x_fit = np.linspace(min(x), max(x), 100)
        y_fit = slope * x_fit + intercept
        
        # Calculate confidence interval
        n = len(x)
        x_mean = x.mean()
        residuals = y - (slope * x + intercept)
        se = np.sqrt(np.sum(residuals**2) / (n - 2))
        t_value = stats.t.ppf(0.975, n - 2)
        uncertainty = t_value * se * np.sqrt(1 + 1/n + (x_fit - x_mean)**2 / np.sum((x - x_mean)**2))
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Plot 1: Calibration curve
        axes[0, 0].scatter(x, y, alpha=0.6, label='Data Points')
        axes[0, 0].plot(x_fit, y_fit, 'r-', linewidth=2, 
                       label=f'Linear Fit (R²={r_value**2:.4f})')
        axes[0, 0].fill_between(x_fit, y_fit - uncertainty, y_fit + uncertainty, 
                               alpha=0.2, color='red', label='95% CI')
        axes[0, 0].set_xlabel(x_col)
        axes[0, 0].set_ylabel(y_col)
        axes[0, 0].set_title('Calibration Curve')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Residuals
        y_pred = slope * x + intercept
        residuals = y - y_pred
        axes[0, 1].scatter(y_pred, residuals, alpha=0.6)
        axes[0, 1].axhline(y=0, color='r', linestyle='--', linewidth=2)
        axes[0, 1].set_xlabel('Predicted Values')
        axes[0, 1].set_ylabel('Residuals')
        axes[0, 1].set_title('Residual Analysis')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Histogram of residuals
        axes[1, 0].hist(residuals, bins=15, edgecolor='black', alpha=0.7)
        axes[1, 0].set_xlabel('Residual Value')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].set_title('Residual Distribution')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Q-Q plot
        stats.probplot(residuals, dist="norm", plot=axes[1, 1])
        axes[1, 1].set_title('Normal Q-Q Plot')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('calibration_analysis.png', dpi=150)
        plt.show()
        
        return {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_value**2,
            'std_error': std_err,
            'p_value': p_value
        }
    
    def plot_control_chart(self, column, subgroup_size=5):
        """Plot control chart"""
        if self.data is None:
            print("No data loaded")
            return
        
        # Get control chart analysis
        results = self.control_chart_analysis(column, subgroup_size)
        
        if results is None:
            return
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 1, figsize=(12, 8))
        
        # X-bar chart
        axes[0].plot(results['subgroup_means'], marker='o', linewidth=2, label='Subgroup Means')
        axes[0].axhline(y=results['x_bar'], color='g', linestyle='-', linewidth=2, label='Center Line')
        axes[0].axhline(y=results['UCL_x'], color='r', linestyle='--', linewidth=2, label='UCL')
        axes[0].axhline(y=results['LCL_x'], color='r', linestyle='--', linewidth=2, label='LCL')
        
        # Mark out-of-control points
        if results['out_of_control_x']:
            axes[0].scatter(results['out_of_control_x'], 
                          [results['subgroup_means'][i] for i in results['out_of_control_x']],
                          color='red', s=100, zorder=5, label='Out of Control')
        
        axes[0].set_xlabel('Subgroup')
        axes[0].set_ylabel('Mean')
        axes[0].set_title('X-bar Control Chart')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # R chart
        axes[1].plot(results['subgroup_ranges'], marker='o', linewidth=2, label='Subgroup Ranges')
        axes[1].axhline(y=results['r_bar'], color='g', linestyle='-', linewidth=2, label='Center Line')
        axes[1].axhline(y=results['UCL_r'], color='r', linestyle='--', linewidth=2, label='UCL')
        axes[1].axhline(y=results['LCL_r'], color='r', linestyle='--', linewidth=2, label='LCL')
        
        # Mark out-of-control points
        if results['out_of_control_r']:
            axes[1].scatter(results['out_of_control_r'],
                          [results['subgroup_ranges'][i] for i in results['out_of_control_r']],
                          color='red', s=100, zorder=5, label='Out of Control')
        
        axes[1].set_xlabel('Subgroup')
        axes[1].set_ylabel('Range')
        axes[1].set_title('R Control Chart')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('control_chart.png', dpi=150)
        plt.show()
    
    def generate_analysis_report(self):
        """Generate comprehensive analysis report"""
        report = """
╔══════════════════════════════════════════════════════════════╗
║           CALIBRATION DATA ANALYSIS REPORT                  ║
╚══════════════════════════════════════════════════════════════╝

Analysis Date: {date}

────────────────────────────────────────────────────────────────

DATA SUMMARY
────────────────────────────────────────────────────────────────
Total Samples: {n_samples}
Variables Analyzed: {n_variables}
Missing Values: {missing_values}

────────────────────────────────────────────────────────────────

DESCRIPTIVE STATISTICS
────────────────────────────────────────────────────────────────
""".format(date=datetime.now().strftime('%Y-%m-%d'),
          n_samples=len(self.data) if self.data is not None else 0,
          n_variables=len(self.data.columns) if self.data is not None else 0,
          missing_values=self.data.isnull().sum().sum() if self.data is not None else 0)
        
        # Add descriptive statistics if available
        if 'descriptive_statistics' in self.analysis_results:
            for col, stats in self.analysis_results['descriptive_statistics'].items():
                report += f"\n{col}:\n"
                report += f"  Mean: {stats['mean']:.4f}\n"
                report += f"  Std Dev: {stats['std']:.4f}\n"
                report += f"  CV: {stats['cv']:.2f}%\n"
                report += f"  Range: {stats['range']:.4f}\n"
        
        report += """
────────────────────────────────────────────────────────────────

OUTLIER ANALYSIS
────────────────────────────────────────────────────────────────
"""
        
        # Add outlier analysis if available
        outlier_keys = [k for k in self.analysis_results.keys() if k.startswith('outliers_')]
        for key in outlier_keys:
            results = self.analysis_results[key]
            col = key.split('_')[1]
            method = key.split('_')[2]
            report += f"\n{col} ({method} method):\n"
            report += f"  Outliers Found: {results['n_outliers']}\n"
            report += f"  Percentage: {results['outlier_percentage']:.2f}%\n"
        
        report += """
────────────────────────────────────────────────────────────────

NORMALITY TESTS
────────────────────────────────────────────────────────────────
"""
        
        # Add normality tests if available
        normality_keys = [k for k in self.analysis_results.keys() if k.startswith('normality_')]
        for key in normality_keys:
            results = self.analysis_results[key]
            col = key.split('_')[1]
            report += f"\n{col}:\n"
            report += f"  Shapiro-Wilk p-value: {results['shapiro_wilk']['p_value']:.4f}\n"
            report += f"  D'Agostino p-value: {results['dagostino_pearson']['p_value']:.4f}\n"
            report += f"  Normal Distribution: {'Yes' if results['is_normal'] else 'No'}\n"
        
        report += """
────────────────────────────────────────────────────────────────

CONTROL CHART ANALYSIS
────────────────────────────────────────────────────────────────
"""
        
        # Add control chart analysis if available
        control_keys = [k for k in self.analysis_results.keys() if k.startswith('control_chart_')]
        for key in control_keys:
            results = self.analysis_results[key]
            col = key.split('_')[2]
            report += f"\n{col}:\n"
            report += f"  Process in Control: {'Yes' if results['process_in_control'] else 'No'}\n"
            report += f"  Out of Control Points (X): {len(results['out_of_control_x'])}\n"
            report += f"  Out of Control Points (R): {len(results['out_of_control_r'])}\n"
        
        report += """
────────────────────────────────────────────────────────────────

RECOMMENDATIONS
────────────────────────────────────────────────────────────────
1. Review any outliers identified in the analysis
2. Verify normality assumptions for statistical tests
3. Monitor control charts for process stability
4. Update calibration procedures based on findings
5. Document all analysis results for audit trail

────────────────────────────────────────────────────────────────

Prepared by: Calibration Data Analysis System
Date: {date}

────────────────────────────────────────────────────────────────
""".format(date=datetime.now().strftime('%Y-%m-%d'))
        
        return report


def main():
    """Main function to demonstrate calibration data analysis"""
    print("=" * 60)
    print("Calibration Data Analysis - Chemical Engineering Project")
    print("=" * 60)
    
    # Create analyzer instance
    analyzer = CalibrationDataAnalyzer()
    
    # Load data
    print("\n1. Loading Calibration Data")
    print("-" * 60)
    data = analyzer.load_calibration_data()
    print(f"Loaded {len(data)} samples with {len(data.columns)} variables")
    
    # Descriptive statistics
    print("\n2. Calculating Descriptive Statistics")
    print("-" * 60)
    stats = analyzer.descriptive_statistics(['concentration_mgL', 'absorbance', 'temperature_C', 'pH'])
    
    for col, stat in stats.items():
        print(f"\n{col}:")
        print(f"  Mean: {stat['mean']:.4f}")
        print(f"  Std Dev: {stat['std']:.4f}")
        print(f"  CV: {stat['cv']:.2f}%")
    
    # Correlation analysis
    print("\n3. Performing Correlation Analysis")
    print("-" * 60)
    corr_results = analyzer.correlation_analysis('concentration_mgL', 'absorbance')
    print(f"Correlation Coefficient: {corr_results['correlation_coefficient']:.4f}")
    print(f"R-squared: {corr_results['r_squared']:.4f}")
    print(f"Slope: {corr_results['slope']:.4f}")
    print(f"Intercept: {corr_results['intercept']:.4f}")
    
    # Outlier detection
    print("\n4. Detecting Outliers")
    print("-" * 60)
    outlier_results = analyzer.outlier_detection('absorbance', method='zscore', threshold=3)
    print(f"Outliers Found: {outlier_results['n_outliers']}")
    print(f"Percentage: {outlier_results['outlier_percentage']:.2f}%")
    
    # Normality test
    print("\n5. Testing Normality")
    print("-" * 60)
    normality_results = analyzer.normality_test('absorbance')
    print(f"Shapiro-Wilk p-value: {normality_results['shapiro_wilk']['p_value']:.4f}")
    print(f"D'Agostino p-value: {normality_results['dagostino_pearson']['p_value']:.4f}")
    print(f"Normal Distribution: {'Yes' if normality_results['is_normal'] else 'No'}")
    
    # ANOVA analysis
    print("\n6. Performing ANOVA Analysis")
    print("-" * 60)
    anova_results = analyzer.anova_analysis('absorbance', 'operator')
    print(f"F-statistic: {anova_results['f_statistic']:.4f}")
    print(f"p-value: {anova_results['p_value']:.4f}")
    print(f"Significant Difference: {'Yes' if anova_results['significant'] else 'No'}")
    
    # Control chart analysis
    print("\n7. Analyzing Control Charts")
    print("-" * 60)
    control_results = analyzer.control_chart_analysis('absorbance', subgroup_size=5)
    print(f"Process in Control: {'Yes' if control_results['process_in_control'] else 'No'}")
    print(f"Out of Control Points (X): {len(control_results['out_of_control_x'])}")
    print(f"Out of Control Points (R): {len(control_results['out_of_control_r'])}")
    
    # Measurement system analysis
    print("\n8. Performing Measurement System Analysis")
    print("-" * 60)
    msa_results = analyzer.measurement_system_analysis(['absorbance'], 'operator')
    print(f"% Gage R&R: {msa_results['percent_gage_rr']:.2f}%")
    print(f"Measurement System Acceptable: {'Yes' if msa_results['measurement_system_acceptable'] else 'No'}")
    
    # Plot calibration curve
    print("\n9. Plotting Calibration Curve")
    print("-" * 60)
    plot_results = analyzer.plot_calibration_curve('concentration_mgL', 'absorbance',
                                                   "Calibration Curve Analysis")
    print(f"Plot saved as 'calibration_analysis.png'")
    
    # Plot control chart
    print("\n10. Plotting Control Charts")
    print("-" * 60)
    analyzer.plot_control_chart('absorbance', subgroup_size=5)
    print(f"Control charts saved as 'control_chart.png'")
    
    # Generate report
    print("\n11. Generating Analysis Report")
    print("-" * 60)
    report = analyzer.generate_analysis_report()
    print(report)
    
    print("\n" + "=" * 60)
    print("Calibration Data Analysis completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    import os
    main()
