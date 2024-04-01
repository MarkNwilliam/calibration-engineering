"""
Quality Management System - Chemical Engineering Project
Demonstrates ISO 9001/ISO 17025 compliance and calibration record management
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import os


class QualityManagementSystem:
    """Quality Management System for calibration laboratory"""
    
    def __init__(self, lab_name="Chemical Engineering Calibration Lab"):
        self.lab_name = lab_name
        self.calibration_records = []
        self.standards_inventory = []
        self.procedures = []
        self.audit_records = []
        
    def create_calibration_record(self, instrument_id, instrument_name, 
                                 calibration_date, next_calibration,
                                 standards_used, measurements, 
                                 environmental_conditions, technician):
        """Create a new calibration record"""
        record = {
            'record_id': f"CAL-{len(self.calibration_records)+1:04d}",
            'instrument_id': instrument_id,
            'instrument_name': instrument_name,
            'calibration_date': calibration_date,
            'next_calibration': next_calibration,
            'standards_used': standards_used,
            'measurements': measurements,
            'environmental_conditions': environmental_conditions,
            'technician': technician,
            'status': 'pending_review',
            'created_at': datetime.now().isoformat()
        }
        
        # Calculate combined uncertainty
        record['combined_uncertainty'] = self.calculate_combined_uncertainty(measurements)
        
        # Determine pass/fail
        record['pass_fail'] = self.evaluate_calibration(record)
        
        self.calibration_records.append(record)
        return record
    
    def calculate_combined_uncertainty(self, measurements):
        """Calculate combined uncertainty from all measurements"""
        uncertainties = []
        for measurement in measurements:
            if 'uncertainty' in measurement:
                uncertainties.append(measurement['uncertainty'])
        
        if uncertainties:
            return np.sqrt(sum([u**2 for u in uncertainties]))
        return 0.0
    
    def evaluate_calibration(self, record):
        """Evaluate if calibration passes acceptance criteria"""
        # Example acceptance criteria
        criteria = {
            'max_uncertainty': 0.05,
            'min_r_squared': 0.99
        }
        
        # Check uncertainty
        if record['combined_uncertainty'] > criteria['max_uncertainty']:
            return 'fail'
        
        # Check R-squared if available
        for measurement in record['measurements']:
            if 'r_squared' in measurement:
                if measurement['r_squared'] < criteria['min_r_squared']:
                    return 'fail'
        
        return 'pass'
    
    def add_standard_to_inventory(self, standard_id, description, 
                                 certificate_number, calibration_date,
                                 next_calibration, uncertainty):
        """Add a standard to the inventory"""
        standard = {
            'standard_id': standard_id,
            'description': description,
            'certificate_number': certificate_number,
            'calibration_date': calibration_date,
            'next_calibration': next_calibration,
            'uncertainty': uncertainty,
            'status': 'active',
            'added_date': datetime.now().isoformat()
        }
        
        self.standards_inventory.append(standard)
        return standard
    
    def check_standard_validity(self, standard_id):
        """Check if a standard is still valid"""
        for standard in self.standards_inventory:
            if standard['standard_id'] == standard_id:
                next_cal = datetime.fromisoformat(standard['next_calibration'])
                if datetime.now() > next_cal:
                    standard['status'] = 'expired'
                    return False, "Standard has expired"
                return True, "Standard is valid"
        return False, "Standard not found"
    
    def create_procedure(self, procedure_id, title, version, 
                        effective_date, content, author):
        """Create a calibration procedure"""
        procedure = {
            'procedure_id': procedure_id,
            'title': title,
            'version': version,
            'effective_date': effective_date,
            'content': content,
            'author': author,
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }
        
        self.procedures.append(procedure)
        return procedure
    
    def create_audit_record(self, audit_date, auditor, scope, 
                           findings, corrective_actions):
        """Create an audit record"""
        audit = {
            'audit_id': f"AUD-{len(self.audit_records)+1:04d}",
            'audit_date': audit_date,
            'auditor': auditor,
            'scope': scope,
            'findings': findings,
            'corrective_actions': corrective_actions,
            'status': 'open',
            'created_at': datetime.now().isoformat()
        }
        
        self.audit_records.append(audit)
        return audit
    
    def generate_calibration_certificate(self, record):
        """Generate a calibration certificate"""
        certificate = f"""
╔══════════════════════════════════════════════════════════════╗
║                    CALIBRATION CERTIFICATE                  ║
╚══════════════════════════════════════════════════════════════╝

Laboratory: {self.lab_name}
Certificate Number: {record['record_id']}
Date of Issue: {datetime.now().strftime('%Y-%m-%d')}

────────────────────────────────────────────────────────────────

INSTRUMENT DETAILS
────────────────────────────────────────────────────────────────
Instrument ID: {record['instrument_id']}
Instrument Name: {record['instrument_name']}
Calibration Date: {record['calibration_date']}
Next Calibration Due: {record['next_calibration']}

────────────────────────────────────────────────────────────────

CALIBRATION STANDARDS USED
────────────────────────────────────────────────────────────────
"""
        
        for standard in record['standards_used']:
            certificate += f"• {standard['id']}: {standard['description']}\n"
            certificate += f"  Certificate: {standard['certificate']}\n"
            certificate += f"  Uncertainty: ±{standard['uncertainty']}\n\n"
        
        certificate += """
────────────────────────────────────────────────────────────────

CALIBRATION RESULTS
────────────────────────────────────────────────────────────────
"""
        
        for measurement in record['measurements']:
            certificate += f"• {measurement['type']}: {measurement['value']}\n"
            if 'uncertainty' in measurement:
                certificate += f"  Uncertainty: ±{measurement['uncertainty']}\n"
            if 'r_squared' in measurement:
                certificate += f"  R²: {measurement['r_squared']:.6f}\n"
            certificate += "\n"
        
        certificate += f"""
────────────────────────────────────────────────────────────────

UNCERTAINTY STATEMENT
────────────────────────────────────────────────────────────────
Combined Standard Uncertainty: {record['combined_uncertainty']:.6f}
Expanded Uncertainty (k=2): ±{2*record['combined_uncertainty']:.6f}
Confidence Level: 95%

────────────────────────────────────────────────────────────────

ENVIRONMENTAL CONDITIONS
────────────────────────────────────────────────────────────────
Temperature: {record['environmental_conditions'].get('temperature', 'N/A')}
Humidity: {record['environmental_conditions'].get('humidity', 'N/A')}
Pressure: {record['environmental_conditions'].get('pressure', 'N/A')}

────────────────────────────────────────────────────────────────

STATEMENT OF CONFORMITY
────────────────────────────────────────────────────────────────
This instrument has been calibrated in accordance with the procedures
of {self.lab_name} and meets the requirements of ISO/IEC 17025:2017.

Result: {'PASS' if record['pass_fail'] == 'pass' else 'FAIL'}

────────────────────────────────────────────────────────────────

Calibrated by: {record['technician']}
Reviewed by: _________________________
Date: {datetime.now().strftime('%Y-%m-%d')}

────────────────────────────────────────────────────────────────

This certificate is issued in accordance with the laboratory's
quality management system certified to ISO 9001:2015 and
ISO/IEC 17025:2017 standards.
"""
        
        return certificate
    
    def generate_quality_report(self):
        """Generate a quality management report"""
        total_records = len(self.calibration_records)
        passed_records = sum(1 for r in self.calibration_records if r['pass_fail'] == 'pass')
        failed_records = total_records - passed_records
        
        # Calculate statistics
        uncertainties = [r['combined_uncertainty'] for r in self.calibration_records]
        avg_uncertainty = np.mean(uncertainties) if uncertainties else 0
        max_uncertainty = np.max(uncertainties) if uncertainties else 0
        
        # Standards inventory
        active_standards = sum(1 for s in self.standards_inventory if s['status'] == 'active')
        expired_standards = sum(1 for s in self.standards_inventory if s['status'] == 'expired')
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║              QUALITY MANAGEMENT REPORT                      ║
╚══════════════════════════════════════════════════════════════╝

Laboratory: {self.lab_name}
Report Date: {datetime.now().strftime('%Y-%m-%d')}

────────────────────────────────────────────────────────────────

CALIBRATION STATISTICS
────────────────────────────────────────────────────────────────
Total Calibrations: {total_records}
Passed: {passed_records}
Failed: {failed_records}
Pass Rate: {(passed_records/total_records*100):.1f}% (if total_records > 0 else 0)

Average Uncertainty: {avg_uncertainty:.6f}
Maximum Uncertainty: {max_uncertainty:.6f}

────────────────────────────────────────────────────────────────

STANDARDS INVENTORY
────────────────────────────────────────────────────────────────
Total Standards: {len(self.standards_inventory)}
Active: {active_standards}
Expired: {expired_standards}

────────────────────────────────────────────────────────────────

PROCEDURES
────────────────────────────────────────────────────────────────
Total Procedures: {len(self.procedures)}
Active: {sum(1 for p in self.procedures if p['status'] == 'active')}

────────────────────────────────────────────────────────────────

AUDIT STATUS
────────────────────────────────────────────────────────────────
Total Audits: {len(self.audit_records)}
Open Findings: {sum(1 for a in self.audit_records if a['status'] == 'open')}
Closed Findings: {sum(1 for a in self.audit_records if a['status'] == 'closed')}

────────────────────────────────────────────────────────────────

COMPLIANCE STATUS
────────────────────────────────────────────────────────────────
ISO 9001:2015: Compliant
ISO/IEC 17025:2017: Compliant
GUM: Compliant

────────────────────────────────────────────────────────────────

RECOMMENDATIONS
────────────────────────────────────────────────────────────────
1. Review and update calibration procedures quarterly
2. Ensure all standards are within calibration validity
3. Address audit findings within 30 days
4. Maintain calibration records for minimum 5 years
5. Conduct management review annually

────────────────────────────────────────────────────────────────

Prepared by: Quality Management System
Date: {datetime.now().strftime('%Y-%m-%d')}

────────────────────────────────────────────────────────────────
"""
        
        return report
    
    def export_to_json(self, filename):
        """Export all data to JSON file"""
        data = {
            'lab_name': self.lab_name,
            'calibration_records': self.calibration_records,
            'standards_inventory': self.standards_inventory,
            'procedures': self.procedures,
            'audit_records': self.audit_records,
            'export_date': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return f"Data exported to {filename}"
    
    def import_from_json(self, filename):
        """Import data from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.lab_name = data.get('lab_name', self.lab_name)
        self.calibration_records = data.get('calibration_records', [])
        self.standards_inventory = data.get('standards_inventory', [])
        self.procedures = data.get('procedures', [])
        self.audit_records = data.get('audit_records', [])
        
        return f"Data imported from {filename}"


def main():
    """Main function to demonstrate quality management system"""
    print("=" * 60)
    print("Quality Management System - Chemical Engineering Project")
    print("=" * 60)
    
    # Create QMS instance
    qms = QualityManagementSystem("Chemical Engineering Calibration Lab")
    
    # Add standards to inventory
    print("\n1. Adding Standards to Inventory")
    print("-" * 60)
    
    standards = [
        ("STD-001", "pH Buffer pH 7.00", "CERT-2024-001", 
         "2024-01-15", "2025-01-15", 0.005),
        ("STD-002", "pH Buffer pH 4.00", "CERT-2024-002", 
         "2024-01-15", "2025-01-15", 0.005),
        ("STD-003", "Analytical Balance Weight 100g", "CERT-2024-003", 
         "2024-02-01", "2025-02-01", 0.0001),
        ("STD-004", "Temperature Reference 0°C", "CERT-2024-004", 
         "2024-03-01", "2025-03-01", 0.01),
    ]
    
    for std in standards:
        standard = qms.add_standard_to_inventory(*std)
        print(f"Added: {standard['standard_id']} - {standard['description']}")
    
    # Check standard validity
    print("\n2. Checking Standard Validity")
    print("-" * 60)
    
    for std_id in ["STD-001", "STD-002", "STD-003", "STD-004"]:
        valid, message = qms.check_standard_validity(std_id)
        print(f"{std_id}: {message}")
    
    # Create calibration records
    print("\n3. Creating Calibration Records")
    print("-" * 60)
    
    # Record 1: pH Meter
    measurements_ph = [
        {'type': 'pH 4.00 Buffer', 'value': 4.01, 'uncertainty': 0.008},
        {'type': 'pH 7.00 Buffer', 'value': 7.00, 'uncertainty': 0.006},
        {'type': 'pH 10.00 Buffer', 'value': 10.02, 'uncertainty': 0.009},
    ]
    
    standards_used_ph = [
        {'id': 'STD-001', 'description': 'pH Buffer pH 7.00', 
         'certificate': 'CERT-2024-001', 'uncertainty': 0.005},
        {'id': 'STD-002', 'description': 'pH Buffer pH 4.00', 
         'certificate': 'CERT-2024-002', 'uncertainty': 0.005},
    ]
    
    env_conditions = {'temperature': '25.0°C', 'humidity': '45%', 'pressure': '101.3 kPa'}
    
    record1 = qms.create_calibration_record(
        instrument_id="PH-001",
        instrument_name="Mettler Toledo pH Meter",
        calibration_date="2024-03-15",
        next_calibration="2024-09-15",
        standards_used=standards_used_ph,
        measurements=measurements_ph,
        environmental_conditions=env_conditions,
        technician="Mark William Nkugwa"
    )
    
    print(f"Created: {record1['record_id']} - {record1['instrument_name']}")
    print(f"Status: {record1['pass_fail'].upper()}")
    
    # Record 2: Analytical Balance
    measurements_balance = [
        {'type': '100g Weight', 'value': 100.001, 'uncertainty': 0.0002},
        {'type': 'Linearity Check', 'value': 0.9998, 'uncertainty': 0.0001, 'r_squared': 0.9999},
    ]
    
    standards_used_balance = [
        {'id': 'STD-003', 'description': 'Analytical Balance Weight 100g', 
         'certificate': 'CERT-2024-003', 'uncertainty': 0.0001},
    ]
    
    record2 = qms.create_calibration_record(
        instrument_id="BAL-001",
        instrument_name="Sartorius Analytical Balance",
        calibration_date="2024-03-16",
        next_calibration="2025-03-16",
        standards_used=standards_used_balance,
        measurements=measurements_balance,
        environmental_conditions=env_conditions,
        technician="Mark William Nkugwa"
    )
    
    print(f"Created: {record2['record_id']} - {record2['instrument_name']}")
    print(f"Status: {record2['pass_fail'].upper()}")
    
    # Record 3: Temperature Probe
    measurements_temp = [
        {'type': 'Ice Point', 'value': 0.01, 'uncertainty': 0.02},
        {'type': 'Boiling Point', 'value': 99.98, 'uncertainty': 0.03},
    ]
    
    standards_used_temp = [
        {'id': 'STD-004', 'description': 'Temperature Reference 0°C', 
         'certificate': 'CERT-2024-004', 'uncertainty': 0.01},
    ]
    
    record3 = qms.create_calibration_record(
        instrument_id="TEMP-001",
        instrument_name="Fluke Digital Thermometer",
        calibration_date="2024-03-17",
        next_calibration="2024-09-17",
        standards_used=standards_used_temp,
        measurements=measurements_temp,
        environmental_conditions=env_conditions,
        technician="Mark William Nkugwa"
    )
    
    print(f"Created: {record3['record_id']} - {record3['instrument_name']}")
    print(f"Status: {record3['pass_fail'].upper()}")
    
    # Create procedures
    print("\n4. Creating Calibration Procedures")
    print("-" * 60)
    
    procedures = [
        ("SOP-CAL-001", "pH Meter Calibration Procedure", "1.0", 
         "2024-01-01", "Standard operating procedure for pH meter calibration", 
         "Mark William Nkugwa"),
        ("SOP-CAL-002", "Analytical Balance Calibration Procedure", "1.0", 
         "2024-01-01", "Standard operating procedure for balance calibration", 
         "Mark William Nkugwa"),
        ("SOP-CAL-003", "Temperature Probe Calibration Procedure", "1.0", 
         "2024-01-01", "Standard operating procedure for temperature calibration", 
         "Mark William Nkugwa"),
    ]
    
    for proc in procedures:
        procedure = qms.create_procedure(*proc)
        print(f"Created: {procedure['procedure_id']} - {procedure['title']}")
    
    # Create audit record
    print("\n5. Creating Audit Record")
    print("-" * 60)
    
    audit = qms.create_audit_record(
        audit_date="2024-03-20",
        auditor="ISO 9001 Auditor",
        scope="Calibration Laboratory Operations",
        findings=["Minor non-conformance in documentation", 
                 "Recommendation to update procedures"],
        corrective_actions=["Update documentation within 30 days", 
                           "Revise procedures by Q2 2024"]
    )
    
    print(f"Created: {audit['audit_id']} - {audit['scope']}")
    print(f"Findings: {len(audit['findings'])} items")
    
    # Generate certificates
    print("\n6. Generating Calibration Certificates")
    print("-" * 60)
    
    for record in [record1, record2, record3]:
        certificate = qms.generate_calibration_certificate(record)
        print(f"\nCertificate for {record['instrument_name']}:")
        print(certificate[:500] + "...")
    
    # Generate quality report
    print("\n7. Generating Quality Report")
    print("-" * 60)
    
    report = qms.generate_quality_report()
    print(report)
    
    # Export data
    print("\n8. Exporting Data")
    print("-" * 60)
    
    export_result = qms.export_to_json("quality_management_data.json")
    print(export_result)
    
    print("\n" + "=" * 60)
    print("Quality Management System completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
