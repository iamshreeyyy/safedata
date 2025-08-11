import yaml
import pandas as pd

from src.risk_assessment import RiskAssessor
from src.privacy_enhancement import PrivacyEnhancer
from src.utility_measurement import UtilityMeasurer
from src.reporting import ReportGenerator

def main():
    # Load config
    with open("config/config.yaml") as f:
        config = yaml.safe_load(f)

    # Load data
    ra = RiskAssessor(config)
    data = ra.load_data(
        config['data_settings']['input_file'],
        config['data_settings']['ground_truth_file']
    )

    # Step 1: Risk Assessment
    risk_report = ra.generate_risk_report()

    # Step 2: Privacy Enhancement
    pe = PrivacyEnhancer(config)
    protected_data = pe.enhance_privacy(data)
    protected_data.to_csv(config['data_settings']['output_file'], index=False)

    # Step 3: Utility Measurement
    um = UtilityMeasurer(config)
    utility_report = um.generate_utility_report(data, protected_data)

    # Step 4: Reporting
    rg = ReportGenerator(config)
    report_path = rg.generate_report(risk_report, utility_report)
    print(f"Report generated: {report_path}")

if __name__ == "__main__":
    main()
